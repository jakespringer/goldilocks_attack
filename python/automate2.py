import subprocess as sp
import os
from cd import cd

code2seq_directory = '/home/ubuntu/code2seq'

all_perturbed_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/java-small-all'
frequency_perturbed_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/java-small-frequency-10000'
l2_perturbed_prefix = '/home/ubuntu/code2seq_attack_Jake_Springer/data/java-small-l2-10000'

all_prefix = 'java-small-all'
frequency_prefix = 'java-small-frequency-10000'
l2_prefix = 'java-small-l2-10000'

if __name__ == '__main__':
   with cd(code2seq_directory):
       sp.Popen(['bash', 'preprocess2.sh', all_perturbed_prefix + '-single', all_prefix + '-single']).wait()
       sp.Popen(['bash', 'preprocess2.sh', all_perturbed_prefix + '-different', all_prefix + '-different']).wait()
       sp.Popen(['bash', 'preprocess2.sh', all_perturbed_prefix + '-same', all_prefix + '-same']).wait()
       sp.Popen(['bash', 'preprocess2.sh', frequency_perturbed_prefix + '-single', frequency_prefix + '-single']).wait()
       sp.Popen(['bash', 'preprocess2.sh', frequency_perturbed_prefix + '-different', frequency_prefix + '-different']).wait()
       sp.Popen(['bash', 'preprocess2.sh', frequency_perturbed_prefix + '-same', frequency_prefix + '-same']).wait()
       sp.Popen(['bash', 'preprocess2.sh', l2_perturbed_prefix + '-single', l2_prefix + '-single']).wait()
       sp.Popen(['bash', 'preprocess2.sh', l2_perturbed_prefix + '-different', l2_prefix + '-different']).wait()
       sp.Popen(['bash', 'preprocess2.sh', l2_perturbed_prefix + '-same', l2_prefix + '-same']).wait()
