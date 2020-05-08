import os
import subprocess
import time
import utils
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('piano', type=str, help='specify the piano model in use')
args = parser.parse_args()
piano = args.piano

reaper = '"C:\\Program Files\\REAPER (x64)\\reaper.exe"'
dataset_path = "C:\\Users\\Marco\\Desktop\\dataset-generation\\data\\dataset-temp"
template_file = 'reaper_templates\\template_{}.rpp'.format(piano)
project_path = 'data\\reaper\\{}'.format(piano)

utils.create_path(project_path)

p = subprocess.Popen(' '.join([reaper, template_file]), shell=True)
time.sleep(3)
p.kill()
print("template opened!")
import reapy
from reapy import reascript_api as RPR
print("reapy import finished!")

all_midi_files = utils.get_files_by_suffix(dataset_path, '.mid')

for i, file in enumerate(all_midi_files):
    print(i, file)
    midi_file = os.path.join(dataset_path, file)
    project_file = project_path+'\\'+file[:-4]+'.rpp'

    p1 = subprocess.Popen(' '.join(['cp', template_file, project_file]), shell=True)
    p2 = subprocess.Popen(' '.join([reaper, project_file]), shell=True)
    time.sleep(2)
    p1.kill()
    p2.kill()
    print("project_file opened!")
    project = reapy.Project() # get current project

    RPR.InsertMedia(midi_file, 1)
    print("midi loaded!")
    project.save()
    try:
        p.kill()
    except:
        print("")
