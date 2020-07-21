import subprocess as sp
from cd import cd
import os
import sys
import shutil
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--topk', type=int, required=True)
parser.add_argument('--dictionary', required=True)
args = parser.parse_args()

dictionary_size = args.topk
dictionary_type = args.dictionary

if dictionary_type not in ['frequency', 'l2']:
    print('Dictionary type {} is unsupported'.format(dictionary_type))
    exit(1)

# MODIFY THESE PARAMETERS TO FIT YOUR INSTALLATION ###################################################################

# code2seq base directory
code2seq_directory = '/home/ubuntu/code2seq'

# trained model base directory
code2seq_output_dir = os.path.join(code2seq_directory, 'models/java-large-model')

# .release file of trained model
code2seq_model = os.path.join(code2seq_output_dir, 'model_iter52.release')

# below are a number of output files; you can set them to whatever you want
output_dictionary_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/{}-dictionary'.format(dictionary_type)
output_perturbation_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/java-small-{}'.format(dictionary_type)
output_perturbation_type = 'same'
output_preprocess_prefix = dictionary_type

# this is where the final results go
output_results_dir = '/home/ubuntu/code2seq_attack_Jake_Springer/data/results'
#######################################################################################################################

if __name__ == '__main__':
    # generate dictionary
    if dictionary_type == 'frequency':
        dict_script = 'frequency_dictionary.py'
    elif dictionary_type == 'l2':
        dict_script = 'l2_dictionary.py'
    dictionary_path = output_dictionary_prefix + '-' + str(dictionary_size) + '.txt'
    dictionary_output = sp.check_output(['python', dict_script, str(dictionary_size)])
    with open(dictionary_path, 'wb') as f:
        f.write(dictionary_output)

    # perturb dataset
    output_perturbation_path = output_perturbation_prefix + '-' + output_perturbation_type    
    sp.Popen(['python', 'perturb_dataset.py', output_perturbation_path, dictionary_path, output_perturbation_type]).wait()

    # preprocess dataset
    output_preprocess_name = output_preprocess_prefix + '-' + str(dictionary_size)
    with cd(code2seq_directory):
       sp.Popen(['bash', 'preprocess2.sh', output_perturbation_path, output_preprocess_name]).wait()
        
    # remove methods without local variables
    p = sp.check_output(['python', 'remove_nolocalvars.py', os.path.join(code2seq_directory, 'data', output_preprocess_name, output_preprocess_name + '.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', output_preprocess_name, output_preprocess_name + '.test.nolocalvars.c2s'), 'wb').write(p)

    # capture results
    with cd(code2seq_directory):
        os.makedirs(os.path.join(output_results_dir, output_preprocess_name), exist_ok=True)
        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', 
            os.path.join(code2seq_directory, 'data', output_preprocess_name, output_preprocess_name + '.test.nolocalvars.c2s')])
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(output_results_dir, output_preprocess_name, 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(output_results_dir, output_preprocess_name, 'ref.txt'))
        open(os.path.join(output_results_dir, output_preprocess_name, 'results.txt'), 'wb').write(p)
