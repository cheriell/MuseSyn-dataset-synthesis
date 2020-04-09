import subprocess
import time
import pretty_midi as pm
import os
import utils
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import matplotlib
matplotlib.rcParams.update({'font.size': 14})

def copy_all_midis():
    dataset_path = 'C:\\Users\\Marco\\OneDrive - Queen Mary, University of London\\Datasets\\MuseScore sheet music'
    source_folders = ['midi', '002', '003', '004', '005', '006', '007', '008', '009', '010']
    project_path = 'C:\\Users\\Marco\\Desktop\\dataset-generation'
    target_folder = 'data\\all_midis_temp'

    utils.create_path(os.path.join(project_path, target_folder))

    subprocesses = []

    for source_folder in source_folders:
        for file in utils.get_files_by_suffix(os.path.join(dataset_path, source_folder), '.mid'):
            midi_file = os.path.join(dataset_path, source_folder, file)
            target_midi_file = os.path.join(project_path, target_folder, file)
            p = subprocess.Popen(' '.join(['cp', '"'+midi_file+'"', '"'+target_midi_file+'"']))
            subprocesses.append(p)

    time.sleep(0.5)
    for p in subprocesses:
        p.kill()

    return

# copy_all_midis()

all_midis_folder = 'data\\all_midis_temp'
utils.create_path('figures')

time_signature_statistics = np.zeros(4, dtype=int)
pedal_statistics = np.zeros(2, dtype=int)
total_notes = []
durations = []
polyphony_level_max = []
polyphony_level_no_pedal_max = []
polyphony_level_ave = []
polyphony_level_no_pedal_ave = []

for item in os.listdir(all_midis_folder):
    print(item)
    midi_data = pm.PrettyMIDI(os.path.join(all_midis_folder, item))

    time_signature_statistics += utils.classify_time_signature(midi_data)
    pedal_statistics += utils.classify_pedal(midi_data)
    total_notes.append(utils.get_total_notes(midi_data))
    durations.append(midi_data.get_end_time())
    (poly_max, poly_max_no_pedal, poly_ave, poly_ave_no_pedal) = utils.get_polyphony_level(midi_data)
    polyphony_level_max.append(poly_max)
    polyphony_level_no_pedal_max.append(poly_max_no_pedal)
    polyphony_level_ave.append(poly_ave)
    polyphony_level_no_pedal_ave.append(poly_ave_no_pedal)

print('time signature:', time_signature_statistics)
print('pedals:', pedal_statistics)
print('total notes:', np.sum(total_notes))
print('total duration:', np.sum(durations)/3600, 'hours')
print('max poly level among all pieces:', np.max(polyphony_level_max))
print('max poly level among all pieces no pedal:', np.max(polyphony_level_no_pedal_max))
print('ave poly level among all pieces:', np.mean(polyphony_level_ave))
print('ave poly level among all pieces no pedal:', np.mean(polyphony_level_no_pedal_ave))

fig, [[ax, ax2], [ax3, ax4], [ax5, ax6]] = plt.subplots(3, 2, figsize=(12,12))

# subplot 1 - time signature
labels = ['4/4', '3/4', '6/8', 'other']
x = np.arange(len(labels))
width = 0.6
rects = ax.bar(x, time_signature_statistics, width, color='steelblue')
ax.set_ylim(0,np.max(time_signature_statistics)+50)
ax.set_ylabel('music pieces')
ax.set_title('(a)\ntime signature distribution')
ax.set_xticks(x)
ax.set_xticklabels(labels)

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects)

# subplot 2 - pedals
ingredients = ['with pedal', 'without pedal']
data = pedal_statistics

def func(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:d} pieces)".format(pct, absolute)

wedges, texts, autotexts = ax2.pie(data, autopct=lambda pct: func(pct, data))
ax2.legend(wedges, ingredients, loc='center left', bbox_to_anchor=(1,0,0.5,1))
ax2.set_title('(b)\nuse of piano pedal')

# subplot 3 - maximum polyphony level
ax3.hist(polyphony_level_max, bins=54, range=(-0.5, 53.5))
ax3.set_ylabel('music pieces')
ax3.set_xlabel('polyphony level')
ax3.set_title('(c)\nmaximum polyphony level (with pedal)')

# subplot 4 - maximum polyphony level without pedel
ax4.hist(polyphony_level_no_pedal_max, bins=24, range=(1.5, 13.5))
ax4.set_ylabel('music pieces')
ax4.set_xlabel('polyphony level')
ax4.set_title('(d)\nmaximum polyphony level (without pedal)')

# subplot 5 - average polyphony level
ax5.hist(polyphony_level_ave, bins=50)
ax5.set_ylabel('music pieces')
ax5.set_xlabel('polyphony level')
ax5.set_title('(e)\naverage polyphony level (with pedal)')

# subplot 6 - average polyphony level without pedel
ax6.hist(polyphony_level_no_pedal_ave, bins=50)
ax6.set_ylabel('music pieces')
ax6.set_xlabel('polyphony level')
ax6.set_title('(f)\naverage polyphony level (without pedal)')

fig.tight_layout()
plt.show()
fig.savefig('figures\\statistics.pdf')
