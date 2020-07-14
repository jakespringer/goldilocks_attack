import subprocess as sp
from cd import cd
import os
import sys

try:
    assert(len(sys.argv) == 2)
    dictionary_size = int(sys.argv[1])
except:
    print('Usage: python automate_frequency.py [topk]')
    exit(1)

code2seq_directory = '/home/ubuntu/code2seq'
code2seq_output_dir = os.path.join(code2seq_directory, 'models/java-large-model')
code2seq_model = os.path.join(code2seq_output_dir, 'model_iter52.release')

output_dictionary_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/frequency-dictionary'
output_perturbation_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/java-small-frequency'
output_perturbation_type = 'same'
output_preprocess_prefix = 'frequency'
output_results_dir = '/home/ubuntu/code2seq_attack_Jake_Springer/data/results'

if __name__ == '__main__':
    # generate dictionary
    dictionary_path = output_dictionary_prefix + '-' + str(dictionary_size) + '.txt'
    dictionary_output = sp.check_output(['python', 'frequency_dictionary.py', str(dictionary_size)])
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
