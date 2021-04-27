correspondence = {
'AA':   'a',
'AE':   '@',
'AH':   'A',
'AO':   'c',
'AW':   'W',
'AY':   'Y',
'EH':   'E',
'ER':   'R',
'EY':   'e',
'IH':   'I',
'IY':   'i',
'OW':   'o',
'OY':   'O',
'UH':   'U',
'UW':   'u',
'B':    'b',
'CH':   'B',
'D':    'd',
'DH':   'D',
'F':    'f',
'G':    'g',
'HH':   'h',
'JH':   'J',
'K':    'k',
'L':    'l',
'M':    'm',
'N':    'n',
'NG':   'G',
'P':    'p',
'R':    'r',
'S':    's',
'SH':   'S',
'T':    't',
'TH':   'T',
'V':    'v',
'W':    'w',
'Y':    'y',
'Z':    'z',
'ZH':   'Z'
}

translations = []

with open("Assets//common_phonemes.dict", mode='r', encoding='utf-8') as twoplace:
    for line in twoplace:
        line = line.rstrip()
        phonemes = line.split()
        translation = []
        for phoneme in phonemes:
            translation.append(correspondence.get(phoneme))
        translations.append(' '.join(translation))

with open("Assets//common_phonemes_oneplace.dict", mode='w+', encoding='utf-8') as oneplace:
    for translation in translations:
        oneplace.write(translation + '\n')
            




        
