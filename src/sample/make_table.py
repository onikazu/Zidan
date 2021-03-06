import numpy as np
import time

print("start")
start = time.time()
q_table = np.random.uniform(low=-1, high=1, size=(6 ** 6, 6))
print(q_table.dtype)
elapse = time.time() - start
print("end")
print(elapse)
np.save("sample_table.npy", q_table)
