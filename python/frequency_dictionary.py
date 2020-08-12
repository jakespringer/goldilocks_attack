import pickle
import numpy as np
import sys
import argparse
import attack_config

# CHANGE THESE PARAMETERS ###############################################

# path to the dictionary in the dataset
word_dictionary = attack_config.CONFIG['code2seq_model_dataset_dict']

# path to the dictionary in the trained model
model_dictionary = attack_config.CONFIG['code2seq_model'] + '.dict'
#########################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('topk', type=int)
    args = parser.parse_args()
    topk = args.topk
    
    with open('{}'.format(word_dictionary), 'rb') as file:
        subtoken_count = pickle.load(file)
    
    with open('{}'.format(model_dictionary), 'rb') as file:
        _ = pickle.load(file) # ignore first section
        index_to_subtoken = pickle.load(file)
        
    index_to_subtoken_count = np.zeros(len(index_to_subtoken))
    for i in range(len(index_to_subtoken)):
        try:
            index_to_subtoken_count[i] = subtoken_count[index_to_subtoken[i]]
        except:
            pass
    
    index_to_subtoken_count[0] = 1.
    subtoken_freq = index_to_subtoken_count
    
    sorted_subtokens = [ i for i in np.argsort(subtoken_freq)[1:][::-1] if index_to_subtoken[i].isidentifier() and not index_to_subtoken[i] == 'METHOD_NAME' ]
    dictionary = [ index_to_subtoken[x] for x in sorted_subtokens[:topk] ]
    print('\n'.join(dictionary))
