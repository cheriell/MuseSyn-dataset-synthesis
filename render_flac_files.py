import subprocess
import os
import time
import utils
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('piano', type=str, help='specify the piano model in use')
args = parser.parse_args()
piano = args.piano

reaper = '"C:\\Program Files\\REAPER (x64)\\reaper.exe"'
projects_path = 'data\\reaper\\{}'.format(piano)
flac_path = 'data\\flac\\{}'.format(piano)

utils.create_path(flac_path)

processes = []

for project in utils.get_files_by_suffix(projects_path, '.rpp'):
    if os.path.exists(os.path.join(flac_path, project[:-4]+'.flac')):
        continue
    print(project)
    project_file = os.path.join(projects_path, project)
    p = subprocess.Popen(' '.join([reaper, '-renderproject', project_file]))
    time.sleep(12)
    processes.append(p)

print('rendering finished!')

time.sleep(10)
for p in processes:
    p.kill()