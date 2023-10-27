import math 
filename = 'text_3_var_21'   
with open(filename) as file:
    lines = file.readlines()
    #print(stroka, type(stroka))

mylist = []

for j in lines:
    nums = j.strip().split(",")
    for i in range(len(nums)):
        if nums[i] ==  'NA':
            nums[i] = str((int(nums[i-1]) + int(nums[i + 1])) / 2) 
            
    filtred = list()
    for j in nums:
        number = float(j)
        if math.sqrt(number) > 70:
            mylist.append(number)
            
with open('r_text_3_TEST_RESULT.txt', 'w') as result:
    for number in mylist:
        result.write(str(number) + "\n")


