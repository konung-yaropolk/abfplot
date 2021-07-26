from itertools import zip_longest
import numpy as np 
import pyabf


# Consts:

ABF_FILE = '2021_06_08_0018_baselined'
SWEEP_N = 13
STEP = 100
COUNT = 20

MIN_X = 300
MAX_X = 400
BASELINE  = [306, 308]


output_array = list(range(COUNT+1)) # np.array([], float)
abf = pyabf.ABF(ABF_FILE + '.abf')


output_array[0] = abf.sweepX[0: MAX_X-MIN_X].tolist()

for i in range(COUNT):
    abf.setSweep(SWEEP_N, 0, baseline=[BASELINE[0] + STEP*i, BASELINE[1] + STEP*i])
    output_array[i+1] = abf.sweepY[MIN_X + STEP*i : MAX_X + STEP*i].tolist()


np_output_array = np.array(output_array, float)
np_output_array = np.transpose(np_output_array)
np_output_array = np.around(np_output_array, decimals=5)

np.savetxt(ABF_FILE + ".csv", np_output_array, delimiter="|")
print(np_output_array)