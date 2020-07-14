#!/usr/bin/env python

import subprocess as sp

# edit the following parameters to configure the automation script
all_dict = '/home/ubuntu/code2seq_attack_Jake_Springer/data/all_dictionary.txt'
frequency_dict = '/home/ubuntu/code2seq_attack_Jake_Springer/data/frequency_dictionary_10000.txt'
l2_dict = '/home/ubuntu/code2seq_attack_Jake_Springer/data/l2_dictionary_10000.txt'

all_perturbed_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/java-small-all'
frequency_perturbed_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/java-small-frequency-10000'
l2_perturbed_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/java-small-l2-10000'

if __name__ == '__main__':
    print('Starting perturbation process...', end='', flush=True)

    perturb_processes = []
    perturb_processes.append(sp.Popen(['python', 'perturb_dataset.py', all_perturbed_prefix + '-single', all_dict, 'single']))
    perturb_processes.append(sp.Popen(['python', 'perturb_dataset.py', all_perturbed_prefix + '-different', all_dict, 'different']))
    perturb_processes.append(sp.Popen(['python', 'perturb_dataset.py', all_perturbed_prefix + '-same', all_dict, 'same']))
    
    perturb_processes.append(sp.Popen(['python', 'perturb_dataset.py', frequency_perturbed_prefix + '-single', frequency_dict, 'single']))
    perturb_processes.append(sp.Popen(['python', 'perturb_dataset.py', frequency_perturbed_prefix + '-different', frequency_dict, 'different']))
    perturb_processes.append(sp.Popen(['python', 'perturb_dataset.py', frequency_perturbed_prefix + '-same', frequency_dict, 'same']))
    
    perturb_processes.append(sp.Popen(['python', 'perturb_dataset.py', l2_perturbed_prefix + '-single', l2_dict, 'single']))
    perturb_processes.append(sp.Popen(['python', 'perturb_dataset.py', l2_perturbed_prefix + '-different', l2_dict, 'different']))
    perturb_processes.append(sp.Popen(['python', 'perturb_dataset.py', l2_perturbed_prefix + '-same', l2_dict, 'same']))
    
    for process in perturb_processes:
        process.wait()
