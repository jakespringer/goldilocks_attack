import pickle
import numpy as np
import sys


if __name__ == '__main__':
    try:
        topk = int(sys.argv[1])
    except:
        print('frequency_dictionary.py [top k]', file=sys.stderr)
        exit(1)
    
    with open('{}'.format('../data/java-large-model/java-large.dict.c2s'), 'rb') as file:
        subtoken_count = pickle.load(file)
    
    with open('{}'.format('../data/java-large-model/model_iter52.release.dict'), 'rb') as file:
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
