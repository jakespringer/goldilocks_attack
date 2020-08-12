import os

CONFIG = dict()
CONFIG['code2seq_directory'] = '../code2seq'
CONFIG['code2seq_model_dir'] = '../code2seq/models/java-large-model' 
CONFIG['code2seq_model'] = '../code2seq/models/java-large-model/model_iter52.release'
CONFIG['code2seq_model_dataset_dict'] = '../data/java-large.dict.c2s'

CONFIG['input_dataset'] = '../data/java-small/test'

CONFIG['output_vocabulary_prefix'] = '../data/vocabulary'
CONFIG['output_perturbation_prefix'] = '../data/perturbation'
CONFIG['output_results_dir'] = '../data/results'
