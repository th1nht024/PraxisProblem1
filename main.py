"""
@author: Thinh Nguyen, Tom Koryciak, Tom Butenschoen, Robert Schleßmann.
"""

import numpy as np
from scipy.io.wavfile import read
import functools
from matplotlib import pyplot as plt

Fs = 44100
impulsantwort = 'Datei_C.wav'

Fs, array = read(impulsantwort)


def stereo_mono(array):
    try:
        if len(array[1]) == 2:
            array = (array[:, 0] + array[:, 1]) / 2
            return array
    except TypeError:
        pass


stereo_mono(array)
maximalerWert = np.max(array)
array_n = array / maximalerWert
maximalerWert_n = np.max(array_n)

indextupleMaximalerWert = np.where(array_n == maximalerWert_n)
index = functools.reduce(lambda sub, elem: sub * 10 + elem, indextupleMaximalerWert)
array_v = array_n[index[0]:]
array_v_log = 20 * np.log10(abs(array_v))

Energie = np.sum(np.square(array))
print(Energie)

dauer = len(array_v_log) / Fs
samples = 100

# TO FIND TN
TN = 0
TNpoint = 0
length = len(array_v_log)
for n in range(length - samples):
    q = 0
    for p in range(samples):
        if array_v_log[n + p] >= -60:
            q = q + 1
    if q == 0:
        TN = dauer * n / length
        TNpoint = array_v_log[n]
        # print(m)
        break

# TO FIND T5
T5 = 0
T5point = 0
length = len(array_v_log)
for n in range(length - samples):
    q = 0
    for p in range(samples):
        if array_v_log[n + p] >= -5:
            q = q + 1
    if q == 0:
        T5 = dauer * n / length
        T5point = array_v_log[n]
        # print(T5point)
        break

# TO FIND T25
T25 = 0
T25point = 0
length = len(array_v_log)
for n in range(length - samples):
    q = 0
    for p in range(samples):
        if array_v_log[n + p] >= -25:
            q = q + 1
    if q == 0:
        T25 = dauer * n / length
        TNv20 = (T25 - T5) * 3
        T25point = array_v_log[n]
        # print(T25point)
        break

# TO FIND T35
T35 = 0
T35point = 0
length = len(array_v_log)
for n in range(length - samples):
    q = 0
    for p in range(samples):
        if array_v_log[n + p] >= -35:
            q = q + 1
    if q == 0:
        T35 = dauer * n / length
        TNv30 = (T35 - T5) * 2
        T35point = array_v_log[n]
        # print(T30point)
        break

# TO FIND C50
samplec50 = round(Fs * 50 * (10 ** (-3)))
length = len(array_v)
Energievor50 = 0
Energienach50 = 0
for n in range(0, samplec50 + 1):
    Energievor50 = Energievor50 + np.square(array_v[n])
for n in range(samplec50 + 1, length):
    Energienach50 = Energienach50 + np.square(array_v[n])
C50 = round(10 * np.log10(Energievor50 / Energienach50), 2)

# TO FIND C80
samplec80 = round(Fs * 80 * (10 ** (-3)))
length = len(array_v)
Energievor80 = 0
Energienach80 = 0
for n in range(0, samplec80 + 1):
    Energievor80 = Energievor80 + np.square(array_v[n])
for n in range(samplec80 + 1, length):
    Energienach80 = Energienach80 + np.square(array_v[n])
C80 = round(10 * np.log10(Energievor80 / Energienach80), 2)

# TO PRINT OUT
if TN == 0:
    print("Can not measure TN directly")
    print("TN von T20 = ", TNv20, "sekunden")
    print("TN von T30 = ", TNv30, "sekunden")
    print("C50 =", C50, "dB")
    print("C80 =", C80, "dB")
else:
    print("TN =", TN, "sekunden")
    print("TN von T20 = ", TNv20, "sekunden")
    print("TN von T30 = ", TNv30, "sekunden")
    print("C50 =", C50, "dB")
    print("C80 =", C80, "dB")

x = np.arange(0, dauer - dauer / (2 * len(array_v_log)), dauer / len(array_v_log))
y = array_v_log
plt.title("Reverb")
plt.xlabel("Time [s]")
plt.ylabel("Sound level [dB]")
plt.plot(x, y)
plt.show()
