all_words = []
common_words = []
line_count = 0

with open('Assets\\common_words.dict', 'r', encoding='utf-8') as f_common:
    for line in f_common:
        common_words.append(line.rstrip())

with open('Assets\\common_syllables.dict', 'w+', encoding='utf-8') as f_new:
    with open('Assets\\dict_stress.dict', 'r', encoding='utf-8') as f_all:
        for line in f_all:
            digits = []
            ls = line.split(' ',1)
            if ls[0] in common_words:
                line_count += 1
                for i in list(ls[1]):
                    if i.isdigit():
                        digits.append(i)
                f_new.write(str(len(digits)) + '\n')
            

print(len(common_words))
print(common_words[0:9])
print(line_count)
f_new.close()
