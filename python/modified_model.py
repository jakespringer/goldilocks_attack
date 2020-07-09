import numpy as np
import tensorflow as tf

from config import Config
from interactive_predict import InteractivePredictor
from model import Model
from argparse import ArgumentParser
from common import Common
from extractor import Extractor

import _pickle as pickle
import reader

import subprocess
import os

# AttackableModel exposes much of the internal state of Model, and then adds placeholders
# and variables for injecting our own subtoken embedding vectors and then training them
# with gradient descent.
# While there is lots of code, much of it is copied directly from code2seq's Model, and 
# then modified appropriately.
class AttackableModel(Model):
    def __init__(self, config):
        super(AttackableModel, self).__init__(config)
        self.init_attackable_test_graph()

    def init_attackable_test_graph(self):
        if self.predict_queue is None:
            self.holes_vocab_size = 200

            self.predict_queue = reader.Reader(subtoken_to_index=self.subtoken_to_index,
                                               node_to_index=self.node_to_index,
                                               target_to_index=self.target_to_index,
                                               config=self.config, is_evaluating=True)

            self.predict_p = tf.placeholder(tf.string)
            self.target_index_p = tf.placeholder(tf.int32, shape=(1, None))
            self.path_source_indices_p = tf.placeholder(tf.int32, shape=(1, self.config.MAX_CONTEXTS, self.config.MAX_NAME_PARTS))
            self.node_indices_p = tf.placeholder(tf.int32, shape=(1, self.config.MAX_CONTEXTS, self.config.MAX_PATH_LENGTH))
            self.path_target_indices_p = tf.placeholder(tf.int32, shape=(1, self.config.MAX_CONTEXTS, self.config.MAX_NAME_PARTS))
            self.valid_mask_p = tf.placeholder(tf.float32, shape=(1, self.config.MAX_CONTEXTS))
            self.path_source_lengths_p = tf.placeholder(tf.int32, shape=(1, self.config.MAX_CONTEXTS))
            self.path_lengths_p = tf.placeholder(tf.int32, shape=(1, self.config.MAX_CONTEXTS))
            self.path_target_lengths_p = tf.placeholder(tf.int32, shape=(1, self.config.MAX_CONTEXTS))
            

            self.reader_output = self.predict_queue.process_from_placeholder(self.predict_p)
            self.reader_output = {key: tf.expand_dims(tensor, 0) for key, tensor in self.reader_output.items()}
            self.predict_top_indices_op, self.predict_top_scores_op, self._predict_target_index, self.attention_weights_op = \
                self.build_test_graph(self.reader_output)
            self.predict_source_string = self.reader_output[reader.PATH_SOURCE_STRINGS_KEY]
            self.predict_path_string = self.reader_output[reader.PATH_STRINGS_KEY]
            self.predict_path_target_string = self.reader_output[reader.PATH_TARGET_STRINGS_KEY]
            self.predict_target_strings_op = self.reader_output[reader.TARGET_STRING_KEY]
    
            self.initialize_session_variables(self.sess)
            self.saver = tf.train.Saver()
            self.load_model(self.sess)

    def build_test_graph(self, input_tensors):
        self.target_index_from_lines = input_tensors[reader.TARGET_INDEX_KEY]
        self.path_source_indices_from_lines = input_tensors[reader.PATH_SOURCE_INDICES_KEY]
        self.node_indices_from_lines = input_tensors[reader.NODE_INDICES_KEY]
        self.path_target_indices_from_lines = input_tensors[reader.PATH_TARGET_INDICES_KEY]
        self.valid_mask_from_lines = input_tensors[reader.VALID_CONTEXT_MASK_KEY]
        self.path_source_lengths_from_lines = input_tensors[reader.PATH_SOURCE_LENGTHS_KEY]
        self.path_lengths_from_lines = input_tensors[reader.PATH_LENGTHS_KEY]
        self.path_target_lengths_from_lines = input_tensors[reader.PATH_TARGET_LENGTHS_KEY]

        target_index = self.target_index_p
        path_source_indices = self.path_source_indices_p
        node_indices = self.node_indices_p
        path_target_indices = self.path_target_indices_p
        valid_mask = self.valid_mask_p
        path_source_lengths = self.path_source_lengths_p
        path_lengths = self.path_lengths_p
        path_target_lengths = self.path_target_lengths_p

        with tf.variable_scope('model', reuse=self.get_should_reuse_variables()):
            self.subtoken_vocab = tf.get_variable('SUBTOKENS_VOCAB',
                                             shape=(self.subtoken_vocab_size, self.config.EMBEDDINGS_SIZE),
                                             dtype=tf.float32, trainable=False)
            self.target_words_vocab = tf.get_variable('TARGET_WORDS_VOCAB',
                                                 shape=(self.target_vocab_size, self.config.EMBEDDINGS_SIZE),
                                                 dtype=tf.float32, trainable=False)
            self.nodes_vocab = tf.get_variable('NODES_VOCAB',
                                          shape=(self.nodes_vocab_size, self.config.EMBEDDINGS_SIZE),
                                          dtype=tf.float32, trainable=False)
            self.holes_vocab = tf.get_variable('HOLES_VOCAB',
                                          shape=(self.holes_vocab_size, self.config.EMBEDDINGS_SIZE),
                                          dtype=tf.float32, trainable=False)

            self.reset_holes_op = tf.assign(self.holes_vocab, tf.zeros_like(self.holes_vocab))
            self.reset_holes()

            self.batched_contexts = self.compute_contexts(subtoken_vocab=self.subtoken_vocab, nodes_vocab=self.nodes_vocab,
                                                     holes_vocab=self.holes_vocab, 
                                                     source_input=path_source_indices, nodes_input=node_indices,
                                                     target_input=path_target_indices,
                                                     valid_mask=valid_mask,
                                                     path_source_lengths=path_source_lengths,
                                                     path_lengths=path_lengths, path_target_lengths=path_target_lengths,
                                                     is_evaluating=True)

            self.outputs, self.final_states = self.decode_outputs(target_words_vocab=self.target_words_vocab,
                                                        target_input=target_index, batch_size=tf.shape(target_index)[0],
                                                        batched_contexts=self.batched_contexts, valid_mask=valid_mask,
                                                        is_evaluating=True)

        if self.config.BEAM_WIDTH > 0:
            predicted_indices = self.outputs.predicted_ids
            topk_values = self.outputs.beam_search_decoder_output.scores
            attention_weights = [tf.no_op()]
        else:
            predicted_indices = self.outputs.sample_id
            topk_values = tf.constant(1, shape=(1, 1), dtype=tf.float32)
            attention_weights = tf.squeeze(self.final_states.alignment_history.stack(), 1)

        return predicted_indices, topk_values, target_index, attention_weights

    def compute_contexts(self, subtoken_vocab, nodes_vocab, holes_vocab, source_input, nodes_input,
                         target_input, valid_mask, path_source_lengths, path_lengths, path_target_lengths,
                         is_evaluating=False):


        source_input_adjusted = source_input + self.holes_vocab_size * tf.ones_like(source_input)
        target_input_adjusted = target_input + self.holes_vocab_size * tf.ones_like(target_input)

        holed_vocab = tf.concat([holes_vocab, subtoken_vocab], axis=0)

        source_word_embed = tf.nn.embedding_lookup(params=holed_vocab,
                                                   ids=source_input_adjusted, partition_strategy='div')  # (batch, max_contexts, max_name_parts, dim)
        path_embed = tf.nn.embedding_lookup(params=nodes_vocab,
                                            ids=nodes_input)  # (batch, max_contexts, max_path_length+1, dim)
        target_word_embed = tf.nn.embedding_lookup(params=holed_vocab,
                                                   ids=target_input_adjusted, partition_strategy='div')  # (batch, max_contexts, max_name_parts, dim)

        source_word_mask = tf.expand_dims(
            tf.sequence_mask(path_source_lengths, maxlen=self.config.MAX_NAME_PARTS, dtype=tf.float32),
            -1)  # (batch, max_contexts, max_name_parts, 1)
        target_word_mask = tf.expand_dims(
            tf.sequence_mask(path_target_lengths, maxlen=self.config.MAX_NAME_PARTS, dtype=tf.float32),
            -1)  # (batch, max_contexts, max_name_parts, 1)

        source_words_sum = tf.reduce_sum(source_word_embed * source_word_mask,
                                         axis=2)  # (batch, max_contexts, dim)
        path_nodes_aggregation = self.calculate_path_abstraction(path_embed, path_lengths, valid_mask,
                                                                 is_evaluating)  # (batch, max_contexts, rnn_size)
        target_words_sum = tf.reduce_sum(target_word_embed * target_word_mask, axis=2)  # (batch, max_contexts, dim)

        context_embed = tf.concat([source_words_sum, path_nodes_aggregation, target_words_sum],
                                  axis=-1)  # (batch, max_contexts, dim * 2 + rnn_size)
        if not is_evaluating:
            context_embed = tf.nn.dropout(context_embed, self.config.EMBEDDINGS_DROPOUT_KEEP_PROB)

        batched_embed = tf.layers.dense(inputs=context_embed, units=self.config.DECODER_SIZE,
                                        activation=tf.nn.tanh, trainable=not is_evaluating, use_bias=False)

        return batched_embed

    def load_model(self, sess):
        if not sess is None:
            reader = tf.train.NewCheckpointReader(self.config.LOAD_PATH)
            restore_dict = dict()
            for v in tf.global_variables():
                tensor_name = v.name.split(':')[0]
                if reader.has_tensor(tensor_name):
                    restore_dict[tensor_name] = v
                else:
                    pass
                    
            saver = tf.train.Saver(restore_dict)
            sess.run(tf.initialize_all_variables())
            saver.restore(sess, self.config.LOAD_PATH)
            print('Done loading model')
        with open(self.config.LOAD_PATH + '.dict', 'rb') as file:
            if self.subtoken_to_index is not None:
                return
            print('Loading dictionaries from: ' + self.config.LOAD_PATH)
            self.subtoken_to_index = pickle.load(file)
            self.index_to_subtoken = pickle.load(file)
            self.subtoken_vocab_size = pickle.load(file)
    
            self.target_to_index = pickle.load(file)
            self.index_to_target = pickle.load(file)
            self.target_vocab_size = pickle.load(file)
    
            self.node_to_index = pickle.load(file)
            self.index_to_node = pickle.load(file)
            self.nodes_vocab_size = pickle.load(file)
    
            self.num_training_examples = pickle.load(file)
            self.epochs_trained = pickle.load(file)
            saved_config = pickle.load(file)
            self.config.take_model_hyperparams_from(saved_config)
            print('Done loading dictionaries')

    def reset_holes(self):
        self.sess.run(self.reset_holes_op)
