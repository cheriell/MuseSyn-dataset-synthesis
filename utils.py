import os


data_path = "C:\\Users\\Marco\\OneDrive - Queen Mary, University of London\\Datasets\\MuseScore sheet music"

# get all sample piece names
def get_all_midis():
    midi_path = os.path.join(data_path, "MIDI")
    midi_files = os.listdir(midi_path)
    return [os.path.join(midi_path, item) for item in midi_files]


#########################################################
# test
#########################################################


# for item in get_all_samples():
#     print(item)
