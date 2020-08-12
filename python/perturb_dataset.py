import sys
import subprocess
import os
import argparse
import attack_config

# path to the directory of .java files to perturb
input_directory = os.path.abspath(attack_config.CONFIG['input_dataset'])

def process_output(process, project, fname, output_directory):
    out, err = process.communicate()
    if len(err) > 0:
        print('Error with {}/{}:'.format(project, fname), err.decode('utf-8'))
    else:
        os.makedirs(os.path.join(output_directory, project), mode=0o755, exist_ok=True)
        with open(os.path.join(output_directory, project, fname), 'wb') as f:
            f.write(out)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('output')
    parser.add_argument('dictionary')
    parser.add_argument('concat')
    #parser.add_argument('num_adversaries', type=int)
    args = parser.parse_args()

    if args.concat not in ['single', 'same', 'different']:
        print('Concatenation strategy needs to be \"single\", \"same\", or \"different\"', file=sys.stderr)
        exit(1)
    
    java_perturb_jar = '../java/target/rename-variable-1.0-SNAPSHOT-shaded.jar'
    output_directory = args.output
    dictionary = args.dictionary
    perturb_type = args.concat
    
    projects = os.listdir(input_directory)
    
    running = []
    for project in projects:
        project_dir = os.path.join(input_directory, project)
        files = [ filename for filename in os.listdir(project_dir) if filename.endswith('.java') ]
        for fname in files:
            file_path = os.path.join(input_directory, project, fname)
            command = ['java', '-jar', java_perturb_jar, dictionary, file_path, perturb_type]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            running.append((process, project, fname, output_directory))
            if len(running) >= 100:
                for ps, pr, fn, od in running:
                    process_output(ps, pr, fn, od)
                running = []
    for ps, pr, fn, od in running:
        process_output(ps, pr, fn, od)
    running = []
