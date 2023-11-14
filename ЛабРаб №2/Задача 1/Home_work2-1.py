import numpy as np
import json

arr = np.load("matrix_21.npy")

size = len(arr)

sum_num = 0
count = 0
average_sum_num = 0

main_diagonal_summ = 0
average_main_diagonal_summ = 0
count_summ_main_diagonal = 0

side_diagonal_summ = 0
average_side_diagonal = 0
count_summ_side_diagonal = 0

max_number = arr[0][0]
min_number = arr[0][0]

array_stat = dict()
array_stat['sum'] = 0
array_stat['avr'] = 0
array_stat['sumMD'] = 0
array_stat['avrMD'] = 0
array_stat['sumSD'] = 0
array_stat['avrSD'] = 0
array_stat['max'] = 0
array_stat['min'] = 0

for i in range(0, size):
    for j in range(0, size):
        if arr[i][j] > max_number:
            #max_number = arr[i][j]
            array_stat['max'] = arr[i][j]
        elif arr[i][j] < min_number:
            #min_number = arr[i][j]
            array_stat['min'] = arr[i][j] 
            
        sum_num += arr[i][j] # сумма всех элементов
        count += 1 
        if i == j:
            count_summ_main_diagonal += 1
            main_diagonal_summ += arr[i][j]
            average_main_diagonal_summ = main_diagonal_summ / count_summ_main_diagonal
            
    average_sum_num = sum_num / count # среднее арифметическое всех элементов 
    
array_stat['sum'] = sum_num
array_stat['avr'] = average_sum_num

array_stat['sumMD'] = main_diagonal_summ
array_stat['avrMD'] = average_main_diagonal_summ

    
for i in range(0, size):
    for j in range(0, size):  
        if i + j == size - 1:
        #if i + j == size:
            count_summ_side_diagonal += 1
            side_diagonal_summ += arr[i][j]
            average_side_diagonal = side_diagonal_summ / count_summ_side_diagonal
            
array_stat['sumSD'] = side_diagonal_summ
array_stat['avrSD'] = average_side_diagonal


for key in array_stat.keys():
    array_stat[key] = float(array_stat[key]) # приведение к типу float
    
with open ("array_stat.json", "w") as result:
    result.write(json.dumps(array_stat))
    
       
norm_array_stat = np.ndarray((size, size), dtype=float) # создаем новую пустую матрицу 

for i in range(0, size):
    for j in range(0, size):
        norm_array_stat[i][j] = arr[i][j] / array_stat['sum']
      
np.save("norm_array_stat", norm_array_stat)

