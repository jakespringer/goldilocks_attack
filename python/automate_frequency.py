import subprocess as sp
from cd import cd
import os

dictionary_size = 10000

code2seq_directory = '/home/ubuntu/code2seq'

output_dictionary_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/frequency-dictionary'
output_perturbation_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/java-small-frequency'
output_perturbation_type = 'single'
output_preprocess_prefix = 'frequency'

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
    output_preprocess_name = output_preprocess_prefix + '-' = str(dictionary_size)
    with cd(code2seq_directory):
       sp.Popen(['bash', 'preprocess2.sh', output_perturbation_path, output_preprocess_name]).wait()
        
