"""
This way is best at the moment.
"""

import sys

import numpy as np
from matplotlib import pyplot

from takemusic.common import fileio

samplerate, sound = fileio.read_wave(sys.argv[1], nchannels=1)

nsamples_per_sec = 100
slidewidth = int(samplerate/nsamples_per_sec)
windowsize = 2048
bass_cut_freq = 120 #in hz
cutpoint = int(bass_cut_freq*windowsize/samplerate)

threshold = 0.1
count_min = 15

point = 0
bass_count = np.zeros(nsamples_per_sec)
count = 0

bass_list = []

max_freq = samplerate/2
bass_freq_ratio = float(bass_cut_freq)/max_freq
C = 10.0

bass_energy_ratio_sum = 0.0

while(point < sound.shape[0]-windowsize):
    ftdata = np.abs(np.fft.fft(sound[point:point+windowsize]))
    all_energy = np.sum(ftdata)
    if(all_energy == 0.0):
        point += slidewidth
        continue
    bass_energy = np.sum(ftdata[:cutpoint]) 
    sys.stdout.write("{:<20} ".format(bass_energy))
    bass_energy_ratio_sum += bass_energy/all_energy
    average_energy = all_energy*bass_freq_ratio
    sys.stdout.write("{:<20} ".format(average_energy))
    if(bass_energy > average_energy*C and count > count_min):
        sys.stdout.write(" * {}".format(count))
        if(count < nsamples_per_sec):
            bass_count[count] += 1
        count = 0

    sys.stdout.write('\n')
    count += 1

    point += slidewidth

bass_energy_ratio = bass_energy_ratio_sum/count
print("bass energy ratio:{}".format(bass_energy_ratio))
print("C / bass energy ratio:{}".format(C/bass_energy_ratio))
argmax = np.argmax(bass_count)
print("argmax:{}".format(argmax))
print("bpm:{}".format(float(nsamples_per_sec*60)/argmax))
pyplot.plot(np.arange(len(bass_count)), bass_count)
pyplot.show()
