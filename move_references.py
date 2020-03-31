import subprocess
import os
import time
import utils

data_path = "C:\\Users\\Marco\\Downloads\\dataset-test"
midi_path = 'data\\midi'
musicxml_path = 'data\\musicxml'

utils.create_path(midi_path)
utils.create_path(musicxml_path)

processes = []

for file in utils.get_files_by_suffix(data_path, '.mid'):
    midi_file = os.path.join(data_path, file)
    p = subprocess.Popen(' '.join(['mv', midi_file, os.path.join(midi_path, file)]))
    processes.append(p)

for file in utils.get_files_by_suffix(data_path, '.mxl'):
    musicxml_file = os.path.join(data_path, file)
    p = subprocess.Popen(' '.join(['mv', musicxml_file, os.path.join(musicxml_path, file)]))
    processes.append(p)

print('moving finished!')
time.sleep(0.5)
for p in processes:
    p.kill()