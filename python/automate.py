import subprocess as sp
from cd import cd
import os
import sys
import shutil
import argparse
import attack_config


parser = argparse.ArgumentParser()
parser.add_argument('--topk', type=int, required=True)
parser.add_argument('--dictionary', required=True)
parser.add_argument('--type', required=False, default='same')
args = parser.parse_args()

dictionary_size = args.topk
dictionary_type = args.dictionary
output_perturbation_type = args.type

if dictionary_type not in ['frequency', 'l2', 'random', 'l2_single']:
    print('Dictionary type {} is unsupported'.format(dictionary_type))
    exit(1)

# code2seq base directory
code2seq_directory = attack_config.CONFIG['code2seq_directory']

# trained model base directory
code2seq_output_dir = attack_config.CONFIG['code2seq_model_dir']

# trained model
code2seq_model = attack_config.CONFIG['code2seq_model']

# below are a number of output files; you can set them to whatever you want
output_dictionary_prefix = attack_config.CONFIG['output_vocabulary_prefix'] + '-' + dictionary_type + '-' + str(dictionary_size)
output_perturbation_prefix = attack_config.CONFIG['output_perturbation_prefix'] + '-' + dictionary_type + '-' + output_perturbation_type + '-' + str(dictionary_size)
output_preprocess_prefix = dictionary_type

# this is where the final results go
output_results_dir = attack_config.CONFIG['output_results_dir']

if __name__ == '__main__':
    # generate dictionary
    print('Generating dictionary')
    if dictionary_type == 'frequency':
        dict_script = 'frequency_dictionary.py'
    elif dictionary_type == 'l2':
        dict_script = 'l2_dictionary.py'
    elif dictionary_type == 'random':
        dict_script = 'all_dictionary.py'
    elif dictionary_type == 'l2_single':
        dict_script = 'l2_single_dictionary.py'
    dictionary_path = output_dictionary_prefix + '-' + str(dictionary_size) + '.txt'
    dictionary_output = sp.check_output(['python', dict_script, str(dictionary_size)])
    with open(dictionary_path, 'wb') as f:
        f.write(dictionary_output)

    # perturb dataset
    print('Perturbing dataset')
    output_perturbation_path = output_perturbation_prefix 
    sp.Popen(['python', 'perturb_dataset.py', output_perturbation_path, dictionary_path, output_perturbation_type]).wait()

    # preprocess dataset
    print('Preprocessing dataset')
    output_preprocess_name = output_preprocess_prefix + '-' + output_perturbation_type + '-' + str(dictionary_size)
    with cd(code2seq_directory):
       sp.Popen(['bash', 'preprocess2.sh', output_perturbation_path, output_preprocess_name]).wait()
        
    # remove methods without local variables
    print('Filtering for methods with local variables')
    p = sp.check_output(['python', 'filter_has_local_variables.py', os.path.join(code2seq_directory, 'data', output_preprocess_name, output_preprocess_name + '.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', output_preprocess_name, output_preprocess_name + '.test.localvars.c2s'), 'wb').write(p)

    # capture results
    print('Computing results')
    with cd(code2seq_directory):
        os.makedirs(os.path.join(output_results_dir, output_preprocess_name), exist_ok=True)
        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', 
            os.path.join(code2seq_directory, 'data', output_preprocess_name, output_preprocess_name + '.test.localvars.c2s')])
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(output_results_dir, output_preprocess_name, 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(output_results_dir, output_preprocess_name, 'ref.txt'))
        open(os.path.join(output_results_dir, output_preprocess_name, 'results.txt'), 'wb').write(p)
