import subprocess as sp
from cd import cd
import os
import shutil

code2seq_directory = '/home/ubuntu/code2seq'
code2seq_model = os.path.join(code2seq_directory, 'models/java-large-model/model_iter52.release')
code2seq_output_dir = os.path.join(code2seq_directory, 'models/java-large-model')

automate_output_dir = '/home/ubuntu/code2seq_attack_Jake_Springer/data/results'

all_prefix = 'java-small-all'
frequency_prefix = 'java-small-frequency-10000'
l2_prefix = 'java-small-l2-10000'

if __name__ == '__main__':
    with cd(code2seq_directory):
        os.makedirs(os.path.join(automate_output_dir, all_prefix + '-single'), exist_ok=True)
        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', os.path.join(code2seq_directory, 'data', all_prefix + '-single', all_prefix + '-single.test.nolocalvars.c2s')])
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(automate_output_dir, all_prefix + '-single', 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(automate_output_dir, all_prefix + '-single', 'ref.txt'))
        open(os.path.join(automate_output_dir, all_prefix + '-single', 'results.txt'), 'wb').write(p)

        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', os.path.join(code2seq_directory, 'data', all_prefix + '-different', all_prefix + '-different.test.nolocalvars.c2s')])
        os.makedirs(os.path.join(automate_output_dir, all_prefix + '-different'), exist_ok=True)
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(automate_output_dir, all_prefix + '-different', 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(automate_output_dir, all_prefix + '-different', 'ref.txt'))
        open(os.path.join(automate_output_dir, all_prefix + '-different', 'results.txt'), 'wb').write(p)

        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', os.path.join(code2seq_directory, 'data', all_prefix + '-same', all_prefix + '-same.test.nolocalvars.c2s')])
        os.makedirs(os.path.join(automate_output_dir, all_prefix + '-same'), exist_ok=True)
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(automate_output_dir, all_prefix + '-same', 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(automate_output_dir, all_prefix + '-same', 'ref.txt'))
        open(os.path.join(automate_output_dir, all_prefix + '-same', 'results.txt'), 'wb').write(p)



        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', os.path.join(code2seq_directory, 'data', frequency_prefix + '-single', frequency_prefix + '-single.test.nolocalvars.c2s')])
        os.makedirs(os.path.join(automate_output_dir, frequency_prefix + '-single'), exist_ok=True)
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(automate_output_dir, frequency_prefix + '-single', 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(automate_output_dir, frequency_prefix + '-single', 'ref.txt'))
        open(os.path.join(automate_output_dir, frequency_prefix + '-single', 'results.txt'), 'wb').write(p)

        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', os.path.join(code2seq_directory, 'data', frequency_prefix + '-different', frequency_prefix + '-different.test.nolocalvars.c2s')])
        os.makedirs(os.path.join(automate_output_dir, frequency_prefix + '-different'), exist_ok=True)
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(automate_output_dir, frequency_prefix + '-different', 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(automate_output_dir, frequency_prefix + '-different', 'ref.txt'))
        open(os.path.join(automate_output_dir, frequency_prefix + '-different', 'results.txt'), 'wb').write(p)

        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', os.path.join(code2seq_directory, 'data', frequency_prefix + '-same', frequency_prefix + '-same.test.nolocalvars.c2s')])
        os.makedirs(os.path.join(automate_output_dir, frequency_prefix + '-same'), exist_ok=True)
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(automate_output_dir, frequency_prefix + '-same', 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(automate_output_dir, frequency_prefix + '-same', 'ref.txt'))
        open(os.path.join(automate_output_dir, frequency_prefix + '-same', 'results.txt'), 'wb').write(p)



        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', os.path.join(code2seq_directory, 'data', l2_prefix + '-single', l2_prefix + '-single.test.nolocalvars.c2s')])
        os.makedirs(os.path.join(automate_output_dir, l2_prefix + '-single'), exist_ok=True)
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(automate_output_dir, l2_prefix + '-single', 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(automate_output_dir, l2_prefix + '-single', 'ref.txt'))
        open(os.path.join(automate_output_dir, l2_prefix + '-single', 'results.txt'), 'wb').write(p)

        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', os.path.join(code2seq_directory, 'data', l2_prefix + '-different', l2_prefix + '-different.test.nolocalvars.c2s')])
        os.makedirs(os.path.join(automate_output_dir, l2_prefix + '-different'), exist_ok=True)
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(automate_output_dir, l2_prefix + '-different', 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(automate_output_dir, l2_prefix + '-different', 'ref.txt'))
        open(os.path.join(automate_output_dir, l2_prefix + '-different', 'results.txt'), 'wb').write(p)

        p = sp.check_output(['python', 'code2seq.py', '--load', code2seq_model, '--test', os.path.join(code2seq_directory, 'data', l2_prefix + '-same', l2_prefix + '-same.test.nolocalvars.c2s')])
        os.makedirs(os.path.join(automate_output_dir, l2_prefix + '-same'), exist_ok=True)
        shutil.copyfile(os.path.join(code2seq_output_dir, 'pred.txt'), os.path.join(automate_output_dir, l2_prefix + '-same', 'pred.txt'))
        shutil.copyfile(os.path.join(code2seq_output_dir, 'ref.txt'), os.path.join(automate_output_dir, l2_prefix + '-same', 'ref.txt'))
        open(os.path.join(automate_output_dir, l2_prefix + '-same', 'results.txt'), 'wb').write(p)
