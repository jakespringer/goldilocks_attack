import sys
import subprocess
import os

if len(sys.argv) != 4 or sys.argv[3] not in ['single', 'same', 'different']:
    print('perturb_dataset.py [output] [dictionary] [single|same|different]', file=sys.stderr)
    exit(1)

java_perturb_jar = '../java/target/rename-variable-1.0-SNAPSHOT-shaded.jar'
input_directory = '../data/java-small/test'
output_directory = sys.argv[1]
dictionary = sys.argv[2]
perturb_type = sys.argv[3]

projects = os.listdir(input_directory)

for project in projects:
    project_dir = os.path.join(input_directory, project)
    files = [ filename for filename in os.listdir(project_dir) if filename.endswith('.java') ]
    for fname in files:
        file_path = os.path.join(input_directory, project, fname)
        command = ['java', '-jar', java_perturb_jar, dictionary, file_path, perturb_type]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if len(err) > 0:
            print('Error with {}/{}:'.format(project, fname), err.decode('utf-8'))
        else:
            os.makedirs(os.path.join(output_directory, project), mode=0o755, exist_ok=True)
            with open(os.path.join(output_directory, project, fname), 'wb') as f:
                f.write(out)
