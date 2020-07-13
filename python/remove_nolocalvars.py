import re
import sys

if __name__ == '__main__':
    re_vdid = re.compile(r'VDID[0-9]+,(.+?)\s')
    
    def get_local_variables(line):
        return sorted(list(set(re_vdid.findall(line))))
    
    input_filename = sys.argv[1]
    
    with open(input_filename) as f:
        lines = f.readlines()
    
    for line in lines:
        local_vars = get_local_variables(line)
        if len(local_vars) > 0:
            print(line, end='')
