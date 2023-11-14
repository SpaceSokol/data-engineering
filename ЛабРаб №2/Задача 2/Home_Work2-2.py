import numpy as np
import os

arr = np.load("./matrix_21_2.npy")

size = len(arr)
limit = 521
x = list()
y = list()
z = list()
count = 0

new_arr = np.ndarray((size, size), dtype=float)

for i in range(0, size):
    for j in range(0, size):
        count += 1
        #print(arr[i][j])
        if arr[i][j] > limit:
            x.append(i)
            y.append(j)
            z.append(arr[i][j])
            
np.savez("result", x=x, y=y, z=z)   
np.savez_compressed("result_zip", x=x, y=y, z=z)                      
            
print(f"result     = {os.path.getsize('result.npz')}")
print(f"result_zip = {os.path.getsize('result_zip.npz')}")



