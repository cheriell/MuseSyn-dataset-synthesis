# dataset-generation
project to create large scale AMT dataset using Reaper and Native Instrument

# collecting musicxml

collecting musicxml files from MuseScroe sheet music

# getting midi files

converting musicxml files to midi format using batch converter plugin in MuseScore

# reaper settings

## vst plugin settings

saved as default (Maverick)

for the other two pianos, decrease the reverb volumn master to 5dB

## generating reaper projects

write a python reaper project parser

### Enable python in ReaScript

Anaconda python and 32-bit python doesn't work, install 64-bit python, and add the `python .dll` file to `Options->Preferences->ReaScript`. Now, Reaper can recognize .py files in ReaScript!

To run the file, in `Actions->Show Actions List` load the created .py file, select it, and `Run`!

### setting up reapy

follow [reapy instructions](https://pypi.org/project/python-reapy/).

In the python which Reaper is referred to use (check `which python`), install `reapy`.

    pip install python-reapy

check installation (within Reaper, run `enable_dist_api.py` and it works):

    python -m reapy

test -> open Reaper, in shell, run

    import reapy
    reapy.print("hello world")



## rendering using command line

    "C:\Program Files\REAPER (x64)\reaper.exe" -renderproject C:\Users\Marco\Downloads\test.rpp


