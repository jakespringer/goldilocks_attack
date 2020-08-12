# a quick helper script to reproduce results from the paper
# left as a reference for how to automate the automate script
import subprocess
#for i in [100, 1097, 1808, 2981, 4915, 8103, 13360, 22026, 36316, 59874, 98716, 162755]
#if __name__ == '__main__':
#    for i in [100, 1097, 1808, 2981, 4915, 8103, 13360, 22026, 36316, 59874, 98716, 162755]:
#        subprocess.run(['python', 'automate.py', '--topk', str(i), '--dictionary', 'random'])

for i in [90, 148, 245, 403, 665, 1097, 1808, 2981, 4915, 8103, 13360, 22026, 36316, 59874, 73906]:
#    subprocess.run(['python', 'automate.py', '--topk', str(i), '--dictionary', 'l2', '--type', 'same'])
#    subprocess.run(['python', 'automate.py', '--topk', str(i), '--dictionary', 'frequency', '--type', 'same'])
    subprocess.run(['python', 'automate.py', '--topk', str(i), '--dictionary', 'random', '--type', 'same'])
