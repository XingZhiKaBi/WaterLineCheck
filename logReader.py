import os
import numpy as np

path = ['./stdout.log', './log_stdout1.txt']
if os.path.exists(path[1]):
    file = open(path[1], mode='w', encoding='utf-8').close()
file = open(path[1],mode='w')
for line in open(path[0], "r", encoding='UTF-8'):
    if line.find('WARNING') == -1 and line.find('INFO') != -1:
        file.write(line)
