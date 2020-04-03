import os
import numpy as np


CC_SUSTAIN_PEDAL = 64
pedal_threshold = 64 # pedal value less than this is considered as pedal-off

def get_files_by_suffix(folder, suffix):
    files = [item for item in os.listdir(folder) if item[-len(suffix):]==suffix]
    return files

def create_path(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print("create path error")

def classify_time_signature(midi_data):
    is_44 = 0
    is_43 = 0
    is_86 = 0
    is_other = 0
    for ts in midi_data.time_signature_changes:
        if ts.numerator == 4 and ts.denominator == 4:
            is_44 = 1
        elif ts.numerator == 3 and ts.denominator == 4:
            is_43 = 1
        elif ts.numerator == 6 and ts.denominator == 8:
            is_86 = 1
        else:
            is_other = 1
    return np.array([is_44, is_43, is_86, is_other])

def classify_pedal(midi_data):
    is_pedal = 0
    for inst in midi_data.instruments:
        for cc in [_e for _e in inst.control_changes if _e.number == CC_SUSTAIN_PEDAL]:
            if cc.value >= pedal_threshold:
                is_pedal = 1
                break
    return np.array([is_pedal, 1-is_pedal])

def get_total_notes(midi_data):
    n_notes = 0
    for inst in midi_data.instruments:
        n_notes += len(inst.notes)
    return n_notes


def compare_rolls(roll, roll_no_pedal):
    import matplotlib.pyplot as plt
    fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(15,8))
    ax1.imshow(roll[:,5000:10000], aspect='auto')
    ax2.imshow(roll_no_pedal[:,5000:10000], aspect='auto')
    plt.show()

def get_polyphony_level(midi_data):
    fs = 100
    roll = (midi_data.get_piano_roll(fs)>0).astype(int)
    roll_no_pedal = (midi_data.get_piano_roll(fs, pedal_threshold=None)>0).astype(int)
    # compare_rolls(roll, roll_no_pedal)
    poly = np.sum(roll, axis=0)
    poly_no_pedal = np.sum(roll_no_pedal, axis=0)

    return (np.max(poly), np.max(poly_no_pedal))
