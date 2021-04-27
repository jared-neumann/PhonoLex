import PySimpleGUI as sg
import itertools
from variables import *

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#               WORD/PHONEME/SYLLABLE LISTS                 #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def parse_words(common_words):

    wordlist = []
    
    with open(common_words, mode='r', encoding='utf-8') as w:
        for word in w:
            word.rstrip()
            wordlist.append(word)

    return wordlist

def parse_phonemes(common_phonemes):

    phonemelist = []

    with open(common_phonemes, mode='r', encoding='utf-8') as p:
        for phonemes in p:
            phonemes.rstrip()
            phonemelist.append(phonemes)

    return phonemelist

def parse_syllables(common_syllables):

    syllablelist = []

    with open(common_syllables, mode='r', encoding='utf-8') as s:
        for syllables in s:
            syllables.rstrip()
            syllablelist.append(syllables)

    return syllablelist

wordlist = parse_words("Assets//common_words.dict")
phonemelist = parse_phonemes("Assets//common_phonemes.dict")
syllablelist = parse_syllables("Assets//common_syllables.dict")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#               MISCELLANEOUS FUNCTIONS                     #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#Retrieve the pattern matching mode.
def get_match_pattern(values):

    return values.get('COMBO')

#Retrieve the pattern of phonemes from the passed values.
def get_pattern(values):

    c = 0
    pattern = {}
            
    for i in range(0,8):
        features = Phoneme(values, i).features
        if bool(features) == True:
            pattern[c] = features
            c += 1
        else:
            continue

    return pattern

#Find all ARPABET symbols that contain a given feature.
def get_arpasymbol(feature_set, arpa_features, allow_diphthongs):

    matches = set()

    for i in feature_set:
        for k,v in arpa_features.items():
            if allow_diphthongs == False:
                if i in v and 'diphthong' not in v:
                    matches.add(k)
            else:
                if i in v:
                    matches.add(k)

    return matches

#Find all ARPABET symbols that satisfy all constraints for every index.
def get_allmatches(pattern, allow_diphthongs):

    allmatches = []

    for i in range(0,len(pattern)):

        allprospects = []

        if 'TYPE' in pattern[i]:
            types = pattern[i].get('TYPE')
            allprospects.append(get_arpasymbol(types, arpa_features, allow_diphthongs))
        if 'MANNER' in pattern[i]:
            manners = pattern[i].get('MANNER')
            allprospects.append(get_arpasymbol(manners, arpa_features, allow_diphthongs))
        if 'VOICE' in pattern[i]:
            voices = pattern[i].get('VOICE')
            allprospects.append(get_arpasymbol(voices, arpa_features, allow_diphthongs))
        if 'PLACE' in pattern[i]:
            places = pattern[i].get('PLACE')
            allprospects.append(get_arpasymbol(places, arpa_features, allow_diphthongs))
        if 'HEIGHT' in pattern[i]:
            heights = pattern[i].get('HEIGHT')
            allprospects.append(get_arpasymbol(heights, arpa_features, allow_diphthongs))
        if 'DEPTH' in pattern[i]:
            depths = pattern[i].get('DEPTH')
            allprospects.append(get_arpasymbol(depths, arpa_features, allow_diphthongs))
        if 'SHAPE' in pattern[i]:
            shapes = pattern[i].get('SHAPE')
            allprospects.append(get_arpasymbol(shapes, arpa_features, allow_diphthongs))

        realprospects = [x for x in allprospects if x]

        matches = list(set.intersection(*realprospects))
        allmatches.append(matches)

    return allmatches

def get_words(mode,
              allmatches,
              wordlist, phonemelist, syllablelist,
              min_chars, max_chars,
              min_syl, max_syl):

    words = []

    if mode == 'contain':
        sequences = itertools.product(*allmatches)
        substrings = [' '.join(i) for i in sequences]
        for substring in substrings:
            tracking = 0
            for description in phonemelist:
                if substring in description.rstrip():
                    description_index = phonemelist.index(description, tracking)
                    word = wordlist[description_index].rstrip()
                    syllables = int(syllablelist[description_index].rstrip())
                    if min_chars <= len(word) and len(word) <= max_chars:
                        if min_syl <= syllables and syllables <= max_syl:
                            words.append(word)
                        else:
                            continue
                    else:
                        continue
                tracking += 1
        
    elif mode == 'exactly match':
        sequences = itertools.product(*allmatches)
        substrings = [' '.join(i) for i in sequences]

        for substring in substrings:
            tracking = 0
            for description in phonemelist:
                if substring == description.rstrip():
                    description_index = phonemelist.index(description, tracking)
                    word = wordlist[description_index].rstrip()
                    syllables = int(syllablelist[description_index].rstrip())
                    if min_chars <= len(word) and len(word) <= max_chars:
                        if min_syl <= syllables and syllables <= max_syl:
                            words.append(word)
                        else:
                            continue
                    else:
                        continue
                tracking += 1
    '''
    elif mode == 'begin with':
        #do something
    elif mode == 'end with':
        #do something
    '''
    return words

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#               PHONEME FEATURE CLASS                       #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

class Phoneme():

    def __init__(self, values, i):

        #Type Features
        self.type = values.get('TYPE_%s' % i)
        #Consonant Features
        self.manner = values.get('MANNER_%s' % i)
        self.voice = values.get('VOICE_%s' % i)
        self.place = values.get('PLACE_%s' % i)
        #Vowel Features
        self.height = values.get('HEIGHT_%s' % i)
        self.depth = values.get('DEPTH_%s' % i)
        self.shape = values.get('SHAPE_%s' % i)
        #Create Feature Dictionary
        self.allfeatures = {'TYPE': self.type,
                            'MANNER': self.manner,
                            'VOICE': self.voice,
                            'PLACE': self.place,
                            'HEIGHT': self.height,
                            'DEPTH': self.depth,
                            'SHAPE': self.shape}
        self.features = {k:v for k,v in self.allfeatures.items() if v}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#               LAYOUT: INTRODUCTORY ROW                    #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#ROW 0: Pattern Matching Mode Options
row_0 = [sg.Text(
            "Search for words that",
            size=(15,1)
            ),
        sg.Combo(
            ['contain', 'exactly match', 'begin with', 'end with'],
            default_value='contain',
            size=(12,1),
            key='COMBO'
            ),
        sg.Text(
            'the following pattern:',
            size=(15,1)
            )]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                  PHONEME TYPE LAYOUT                      #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#ROW 1: Phoneme Type Options
row_1 = [sg.Text(
            "Type",
            font=('bold'),
            size=(12,1),
            justification='r'
            )]
for i in range(0,8):
    row_1.append(sg.Listbox(
                    phoneme_types,
                    size=(10,2),
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    no_scrollbar=True,
                    key='TYPE_%s' % i
                    ))
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#               CONSONANT FEATURE LAYOUT                    #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#ROW 2: Manner of Articulation Options
row_2 = [sg.Text(
            "Manner",
            font=('bold'),
            size=(12,1),
            justification='r'
            )]
for i in range(0,8):
    row_2.append(sg.Listbox(
                    consonants_manners,
                    size=(10,8),
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    no_scrollbar=True,
                    key='MANNER_%s' % i
                    ))
    
#ROW 3: Voice Options
row_3 = [sg.Text(
            "Voice",
            font=('bold'),
            size=(12,1),
            justification='r'
            )]
for i in range(0,8):
    row_3.append(sg.Listbox(
                    consonants_voices,
                    size=(10,2),
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    no_scrollbar=True,
                    key='VOICE_%s' % i
                    ))

#ROW 4: Place of Articulation Options
row_4 = [sg.Text(
            "Place",
            font=('bold'),
            size=(12,1),
            justification='r'
            )]
for i in range(0,8):
    row_4.append(sg.Listbox(
                    consonants_places,
                    size=(10,10),
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    no_scrollbar=True,
                    key='PLACE_%s' % i
                    ))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                   VOWEL FEATURE LAYOUT                    #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#ROW 5: Height (Close-Open) Options
row_5 = [sg.Text(
            "Height",
            font=('bold'),
            size=(12,1),
            justification='r'
            )]
for i in range(0,8):
    row_5.append(sg.Listbox(
                    vowels_heights,
                    size=(10,7),
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    no_scrollbar=True,
                    key='HEIGHT_%s' % i
                    ))

#ROW 6: Depth (Front-Back) Options
row_6 = [sg.Text(
            "Depth",
            font=('bold'),
            size=(12,1),
            justification='r'
            )]
for i in range(0,8):
    row_6.append(sg.Listbox(
                    vowels_depths,
                    size=(10,5),
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    no_scrollbar=True,
                    key='DEPTH_%s' % i
                    ))

#ROW 7: Shape (Roundedness) Options
row_7 = [sg.Text(
            "Shape",
            font=('bold'),
            size=(12,1),
            justification='r'
            )]
for i in range(0,8):
    row_7.append(sg.Listbox(
                    vowels_shapes,
                    size=(10,2),
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    no_scrollbar=True,
                    key='SHAPE_%s' % i
                    ))

#ROW 8: Word-Level Options
row_8 = [sg.Text(
            "Word",
            font=('bold'),
            size=(12,1),
            justification='r'
            ),
         sg.Text(
            "Character Length:",
            size=(13,1),
            justification='l'
            ),
         sg.InputText(
            size=(4,1),
            key = "C_MIN"
            ),
         sg.Text(
            "–-",
            size=(1,1),
            justification='c'
            ),
         sg.InputText(
            size=(4,1),
            key = "C_MAX"
            ),
         sg.Text(
            "Syllable Range:",
            size=(11,1),
            justification='c',
            ),
         sg.InputText(
            size=(4,1),
            justification='l',
            key = "S_MIN"
            ),
         sg.Text(
            "–-",
            size=(1,1),
            justification='c'
            ),
         sg.InputText(
            size=(4,1),
            key = "S_MAX"
            ),
         sg.Checkbox(
            "Allow Diphthongs?",
            default = True,
            size = (14,1),
            key="DIPHTHONGS"
            )
         ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                   APP FUNCTION BUTTONS                    #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#ROW 9: Exit and Submit Buttons
row_9 = [sg.CButton(
            'Exit',
            size=(12,1)
            ),
         sg.Button(
            'Search',
            size=(12,1)
            )]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                   main(): CREATE WINDOW                   #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def main():
    #Combine the above elements into the final layout.
    layout = [row_0,
              row_1,
              row_2,
              row_3,
              row_4,
              row_5,
              row_6,
              row_7,
              row_8,
              row_9]    #Also 9 columns: 1 Label + 8 Indices.

    #Finally, create the window object with title and layout.
    window = sg.Window('Phonological Search Engine', layout)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                   main(): EVENT LOOP                      #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event == 'Search':

            allow_diphthongs = values.get('DIPHTHONGS')

            pattern = get_pattern(values)
            allmatches = get_allmatches(pattern, allow_diphthongs)
            mode = get_match_pattern(values)

            if values.get('C_MIN') != '':
                min_chars = int(values.get('C_MIN'))
            else:
                min_chars = 0

            if values.get('C_MAX') != '':
                max_chars = int(values.get('C_MAX'))
            else:
                max_chars = 99

            if values.get('S_MIN') != '':
                min_syl = int(values.get('S_MIN'))
            else:
                min_syl = 0

            if values.get('S_MAX') != '':
                max_syl = int(values.get('S_MAX'))
            else:
                max_syl = 99
                
            results = get_words(mode,
                                allmatches,
                                wordlist, phonemelist, syllablelist,
                                min_chars, max_chars,
                                min_syl, max_syl)

            
            for r in results:
                print(r)

    #Clean up.
    window.close()

if __name__=='__main__':
    main()
