import sys

import numpy as np
from matplotlib import pyplot

from takemusic.common import fileio

samplerate, sound = fileio.read_wave(sys.argv[1], nchannels=1)

nsamples_per_sec = 100
slidewidth = int(samplerate/nsamples_per_sec)
windowsize = 2048
cutfreq = 120 #in hz
cutpoint = int(cutfreq*windowsize/samplerate)

threshold = 0.1
count_min = 15

point = 0
bass_count = [0] * nsamples_per_sec
count = 0

bass_list = []

energy_ratio_max = 0.1
energy_ratio_min = 0.001
energy_cofficient = 1.0/energy_ratio_min
r = int(energy_ratio_max/energy_ratio_min)
energy_ratio_list = [0] * r

while(point < sound.shape[0]-windowsize):
    ftdata = np.abs(np.fft.fft(sound[point:point+windowsize]))
    all_energy = np.sum(ftdata)
    if(all_energy == 0.0):
        point += slidewidth
        continue
    bass = np.sum(ftdata[:cutpoint]) 
    sys.stdout.write("{:<20} ".format(bass))
    energy_ratio = float(bass)/all_energy
    if(energy_ratio > threshold and count > count_min):
        sys.stdout.write(" * {}".format(count))
        if(count < nsamples_per_sec):
            bass_count[count] += 1
        count = 0

    if(energy_ratio < energy_ratio_max):
        energy_ratio_list[int(energy_ratio*energy_cofficient)] += 1

    sys.stdout.write('\n')
    count += 1

    point += slidewidth

#print("on beats:{}".format(float(energy_ratio_sum_on_beats)/on_beats_count))
print("max:{}".format(np.argmax(bass_count)))
pyplot.subplot(211)
pyplot.plot(np.arange(len(energy_ratio_list))/energy_cofficient, 
            energy_ratio_list)
pyplot.subplot(212)
pyplot.plot(np.arange(len(bass_count)), bass_count)


#b = bass_list[int(sys.argv[2]):int(sys.argv[3])]
#pyplot.plot(range(len(b)), b)
pyplot.show()

