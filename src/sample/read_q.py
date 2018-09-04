import numpy as np
import time

print("start")
start = time.time()
np.load("sample_table.npy")
elapse = time.time() - start
print("end")
print(elapse)