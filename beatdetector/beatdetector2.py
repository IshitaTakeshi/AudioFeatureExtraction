import sys

import numpy as np
from matplotlib import pyplot

from takemusic.lib import fileio

samplerate, sound = fileio.read_wave(sys.argv[1], nchannels=1)

nsamples_per_sec = 100
slidewidth = int(samplerate/nsamples_per_sec)
windowsize = 2048
cutfreq = 120 #in hz
cutpoint = int(cutfreq*windowsize/samplerate)

threshold = 700
count_min = 15

point = 0
bass_count = [0] * nsamples_per_sec
count = 0

bass_list = []

energy_ratio_on_beats = 0.0
on_beats_count = 0
energy_ratio_on_no_beats = 0.0
on_no_beats_count = 0

while(point < sound.shape[0]-windowsize):
    ftdata = np.abs(np.fft.fft(sound[point:point+windowsize]))
    all_energy = np.sum(ftdata)
    if(all_energy == 0.0):
        point += slidewidth
        continue
    bass = np.sum(ftdata[:cutpoint])
    
    bass_list.append(bass) 
 
    sys.stdout.write("{:<20} ".format(bass))
    energy_ratio = float(bass)/all_energy
    if(bass > threshold and count > count_min):
        sys.stdout.write(" * {}".format(count))
        if(count < nsamples_per_sec):
            bass_count[count] += 1
        count = 0

        energy_ratio_on_beats += energy_ratio
        on_beats_count += 1
 
    energy_ratio_on_no_beats += energy_ratio
    on_no_beats_count += 1

    sys.stdout.write('\n')
    count += 1

    point += slidewidth
print("on beats:{}".format(float(energy_ratio_on_beats)/on_beats_count))
print("on no beats:{}".format(float(energy_ratio_on_no_beats)/on_no_beats_count))
print("max:{}".format(np.argmax(bass_count)))
pyplot.plot(range(len(bass_count)), bass_count)
#pyplot.plot(range(len(bass_list[1000:3000])), bass_list[1000:3000])
pyplot.show()

