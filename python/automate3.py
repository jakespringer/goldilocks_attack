import subprocess as sp
from cd import cd
import os
import shutil

code2seq_directory = '/home/ubuntu/code2seq'

all_prefix = 'java-small-all'
frequency_prefix = 'java-small-frequency-10000'
l2_prefix = 'java-small-l2-10000'

if __name__ == '__main__':
    p = sp.check_output(['python', 'remove_nolocalvars.py', os.path.join(code2seq_directory, 'data', all_prefix + '-single', all_prefix + '-single.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', all_prefix + '-single', all_prefix + '-single.test.nolocalvars.c2s'), 'wb').write(p)

    p = sp.check_output(['python', 'remove_nolocalvars.py', os.path.join(code2seq_directory, 'data', all_prefix + '-different', all_prefix + '-different.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', all_prefix + '-different', all_prefix + '-different.test.nolocalvars.c2s'), 'wb').write(p)

    p = sp.check_output(['python', 'remove_nolocalvars.py', os.path.join(code2seq_directory, 'data', all_prefix + '-same', all_prefix + '-same.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', all_prefix + '-same', all_prefix + '-same.test.nolocalvars.c2s'), 'wb').write(p)

    p = sp.check_output(['python', 'remove_nolocalvars.py', os.path.join(code2seq_directory, 'data', frequency_prefix + '-single', frequency_prefix + '-single.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', frequency_prefix + '-single', frequency_prefix + '-single.test.nolocalvars.c2s'), 'wb').write(p)

    p = sp.check_output(['python', 'remove_nolocalvars.py', os.path.join(code2seq_directory, 'data', frequency_prefix + '-different', frequency_prefix + '-different.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', frequency_prefix + '-different', frequency_prefix + '-different.test.nolocalvars.c2s'), 'wb').write(p)

    p = sp.check_output(['python', 'remove_nolocalvars.py', os.path.join(code2seq_directory, 'data', frequency_prefix + '-same', frequency_prefix + '-same.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', frequency_prefix + '-same', frequency_prefix + '-same.test.nolocalvars.c2s'), 'wb').write(p)

    p = sp.check_output(['python', 'remove_nolocalvars.py', os.path.join(code2seq_directory, 'data', l2_prefix + '-single', l2_prefix + '-single.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', l2_prefix + '-single', l2_prefix + '-single.test.nolocalvars.c2s'), 'wb').write(p)

    p = sp.check_output(['python', 'remove_nolocalvars.py', os.path.join(code2seq_directory, 'data', l2_prefix + '-different', l2_prefix + '-different.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', l2_prefix + '-different', l2_prefix + '-different.test.nolocalvars.c2s'), 'wb').write(p)

    p = sp.check_output(['python', 'remove_nolocalvars.py', os.path.join(code2seq_directory, 'data', l2_prefix + '-same', l2_prefix + '-same.test.c2s')])
    open(os.path.join(code2seq_directory, 'data', l2_prefix + '-same', l2_prefix + '-same.test.nolocalvars.c2s'), 'wb').write(p)
