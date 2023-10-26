filename = 'text_1_var_21'
with open(filename) as file:
    stroka = file.readlines()
    
word_stat = dict()

for text in stroka:
    new_stroka = (text.strip()
           .replace("!", " ")
           .replace("?", " ")
           .replace(".", " ")
           .replace(",", " ")
           .strip()).split(" ")
    for new_word in new_stroka:
        if new_word in word_stat:
            word_stat[new_word] += 1
        else:
            word_stat[new_word] = 1 
            
word_stat = (dict(sorted(word_stat.items(), reverse=True, key=lambda item: item[1])))
print(word_stat)

with open('text_1_var_21_result.txt', 'w') as result:
    for key, value in word_stat.items():
        result.write(key + ":" + str(value) + "\n")