filename = 'text_2_var_21'
with open(filename) as file:
    stroka = file.readlines()
    
    
count = 0
summ_number = 0
average_value = 0
mylist = []

for i in stroka:
    new_stroka = i.strip().replace(".", " ").strip().split(" ")
    #print(new_stroka)
    len_str = len(new_stroka)
    for j in new_stroka:
        summ_number += int(j)
        count += 1
        #print(new_stroka.index)
        #print(count)
        if  len_str == count:
            average_value = summ_number / count
            mylist.append(average_value)
            count = 0
            len_str = 0
            summ_number = 0
            
            
with open('r_text_2_TEST_RESULT.txt', 'w') as result:
    for number in mylist:
        result.write(str(number) + "\n")

