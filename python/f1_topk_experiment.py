import subprocess

for i in [100, 1097, 1808, 2981, 4915, 8103, 13360, 22026, 36316, 59874, 98716, 162755]
    subprocess.run(['python', 'automate.py', '--topk', str(i), '--dictionary', 'l2'])
