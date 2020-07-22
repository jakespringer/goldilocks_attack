import sys
import subprocess
import os
import re
import itertools
import numpy as np
import tensorflow as tf

from config import Config
from interactive_predict import InteractivePredictor
from model import Model
from modified_model import AttackableModel
from argparse import ArgumentParser

from common import Common
from extractor import Extractor
import reader
import _pickle as pickle

# CHANGE THIS ###################################################
# path to the .release of the trained model
model_release = '/home/jspring1/MIT_Workspace/code2seq/models/java-large-model/model_iter52.release'
#################################################################

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('topk', type=int)
    args = parser.parse_args()
    topk = args.topk
    
    # We want to print to stdout exactly what we want to output, so forward
    # everything else to stderr. Hacky, but works.
    real_stdout = sys.stdout
    sys.stdout = sys.stderr
    
    # Hacky but significantly easier way of loading code2seq --
    # code2seq already runs a significant amount of code to load all
    # of the default parameters appropriately given command line arguments.
    # Therefore, we take advantage of that and inject command line arguemnts
    # to generate the code2seq config.
    parser = ArgumentParser()
    parser.add_argument("-d", "--data", dest="data_path",
                        help="path to preprocessed dataset", required=False)
    parser.add_argument("-te", "--test", dest="test_path",
                        help="path to test file", metavar="FILE", required=False)
    
    parser.add_argument("-s", "--save_prefix", dest="save_path_prefix",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument("-l", "--load", dest="load_path",
                        help="path to saved file", metavar="FILE", required=False)
    parser.add_argument('--release', action='store_true',
                        help='if specified and loading a trained model, release the loaded model for a smaller model '
                             'size.')
    parser.add_argument('--predict', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--seed', type=int, default=239)
    args = parser.parse_args(['--load', model_release,
                '--predict'])
    
    np.random.seed(args.seed)
    tf.set_random_seed(args.seed)
    
    config = Config.get_default_config(args)
    
    # Construct an AttackableModel, which is just a code2seq Model but where we
    # publicize much of the internal state of the model and add a system to 
    # compute and inject embedding vectors.
    model = AttackableModel(config)
    subtoken_vocab = model.sess.run(model.subtoken_vocab)
    subtoken_mag = np.linalg.norm(subtoken_vocab, axis=1)
    index_to_subtoken = model.index_to_subtoken
    
    sorted_subtokens = [ i for i in np.argsort(subtoken_mag)[::-1] if index_to_subtoken[i].isidentifier() and not index_to_subtoken[i] == 'METHOD_NAME' ]
    dictionary = [ index_to_subtoken[x] for x in sorted_subtokens[:topk] ]
    sys.stdout = real_stdout
    print('\n'.join(dictionary))
