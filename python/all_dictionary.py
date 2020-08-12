import pickle
import numpy as np
import sys
import argparse
import random
import attack_config


# path to the dictionary in the trained model
model_dictionary = attack_config.CONFIG['code2seq_model'] + '.dict'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('topk', type=int)
    args = parser.parse_args()
    topk = args.topk
    
    with open('{}'.format(model_dictionary), 'rb') as file:
        _ = pickle.load(file) # ignore first section
        index_to_subtoken = pickle.load(file)
        
    subtokens = [x for x in sorted(index_to_subtoken.values()) if x.isidentifier() and not x == 'METHOD_NAME']
    random.seed(1)
    random.shuffle(subtokens)
    print('\n'.join(subtokens[:topk]))
