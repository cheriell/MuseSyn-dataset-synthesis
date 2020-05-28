import warnings
warnings.filterwarnings('ignore')
import subprocess
import os
import time
import utils
import argparse
import pretty_midi as pm

parser = argparse.ArgumentParser()
parser.add_argument('piano', type=str, help='specify the piano model in use')
args = parser.parse_args()
piano = args.piano

reaper = '"C:\\Program Files\\REAPER (x64)\\reaper.exe"'
projects_path = 'data\\reaper\\{}'.format(piano)
flac_path = 'data\\flac\\{}'.format(piano)

utils.create_path(flac_path)

processes = []

count = 0
for i, project in enumerate(utils.get_files_by_suffix(projects_path, '.rpp')):
    if os.path.exists(os.path.join(flac_path, project[:-4]+'.flac')):
        continue
    print(i, project)
    project_file = os.path.join(projects_path, project)
    p = subprocess.Popen(' '.join([reaper, '-renderproject', project_file]))
    midi_data = pm.PrettyMIDI('data/dataset-temp/'+project[:-3]+'mid')
    music_length = midi_data.get_end_time()
    print('music length:', music_length)
    time.sleep(music_length / 25)
    processes.append(p)
    
    if count % 5 == 4:
        print('rest for a while...')
        time.sleep(10)
        for p in processes:
            p.kill()
        print('continue rendering~~~')
    count += 1

print('rendering finished!')

time.sleep(10)
try:
    for p in processes:
        p.kill()
    print('exit')
except:
    print('exit')