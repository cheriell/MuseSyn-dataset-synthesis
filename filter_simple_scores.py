from music21.stream import Measure
from music21.note import Note
from music21.chord import Chord
from music21 import converter
import numpy as np
import os
import time
import subprocess

raw_dataset_path = 'C:\\Users\\Marco\\OneDrive - Queen Mary, University of London\\Datasets\\MusicScore Dataset\\raw_scores'
simple_scores = []
ps = []

for item_index, item in enumerate(os.listdir(raw_dataset_path)):
    print(item_index, item)
    s = converter.parse(os.path.join(raw_dataset_path, item))
    part_right, part_left = tuple(s.parts)
    simple = True
    for ms in [part_right.getElementsByClass(Measure)] + [part_left.getElementsByClass(Measure)]:
        for nt in ms.flat.notesAndRests:
            if nt.duration.quarterLength % 0.125 != 0:
                print(nt, nt.duration.quarterLength)
                print()
                simple = False
                break
        if not simple:
            break
    if simple:
        simple_scores.append(item_index)
        p = subprocess.Popen(' '.join(['cp', os.path.join('C:\\Users\\Marco\\"OneDrive - Queen Mary, University of London"\\Datasets\\"MusicScore Dataset"\\raw_scores', item), 'C:\\Users\\Marco\\"OneDrive - Queen Mary, University of London"\\Datasets\\"MusicScore Dataset"\\simple_scores']))
        time.sleep(0.05)
        ps.append(p)

print('N simple scores:', len(simple_scores))
for p in ps:
    p.kill()