from dafsa import DAFSA

dictionary = []

with open("Assets//common_phonemes_oneplace.dict", mode='r', encoding='utf-8') as d:
    for line in d:
        line = line.rstrip()
        dictionary.append(line)

dawg = DAFSA(dictionary)

with open('dawg.png', mode='w+') as f:
    dawg.write_figure(f)
