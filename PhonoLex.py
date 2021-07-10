import json
import pandas as pd

class Phonology():
    
    vocabulary = None
    features = None
    
    @classmethod
    def load_vocabulary(cls, vocabulary_path):
        with open(vocabulary_path) as in_file:
            cls.vocabulary = json.load(in_file)
        in_file.close()
        return cls.vocabulary
    
    @classmethod
    def load_features(cls, features_path):
        with open(features_path) as in_file:
            cls.features = json.load(in_file)
        in_file.close()
        return cls.features
    
    def __init__(self, vocabulary_path = 'data/cmu.json', features_path = 'data/features.json'):
        if self.vocabulary == None:
            self.vocabulary = self.load_vocabulary(vocabulary_path)
        if self.features == None:
            self.features = self.load_features(features_path)
    
    # Describes the first instance of the string found in the vocabulary.
    def describe(self, word):
        
        if self.is_word(word):
            is_word = True
        else:
            is_word = False
            
        number_of_syllables = self.number_of_syllables(word)
        diphthongs = self.contains_diphthongs(word)
        character_length = self.character_length(word)
        phone_length = self.phone_length(word)
        phones_with_stress = self.phones_with_stress(word)
        phones_without_stress = self.phones_without_stress(word)
        feature_set = self.feature_set(word)
            
        return {'word': word,
                 'is_word': is_word, 
                 'syllables': number_of_syllables,
                 'diphthongs': diphthongs,
                 'characters': character_length,
                 'phonemes': phone_length,
                 'phones with stress': phones_with_stress, 
                 'phones without stress': phones_without_stress,
                 'features': feature_set}
    
    def description_table(self, word):
        
        description = self.describe(word)
        
        #First Table
        first_table = {'word': description['word'],
                       'is_word': description['is_word'], 
                       'syllables': description['syllables'],
                       'diphthongs': description['diphthongs'],
                       'characters': description['characters'],
                       'phonemes': description['phonemes']}
        
        df1 = pd.DataFrame.from_dict(first_table, orient='index')
        df1 = df1.rename(columns={0:""})
        print()
        print('Table 1: Word-Level Features')
        print(df1)
        
        #Second Table
        if self.is_word(word):
            df2 = pd.DataFrame.from_dict(description['features'])
        
            new_indices = {}
            for i in range(0, len(description['phones with stress'])):
                new_indices[i] = description['phones with stress'][i]
        
            df2 = df2.rename(index=new_indices)
            df2 = df2.T
            print()
            print('Table 2: Phoneme-Level Features')
            print(df2)
            
    def is_word(self, word):
        if word.lower() in self.vocabulary:
            return True
        return False
    
    def number_of_syllables(self, word):
        
        number_of_syllables = 0
        
        if self.is_word(word):
            phones = self.phones_with_stress(word)
        
            for phone in phones:
                if any(x.isdigit() for x in phone):
                    number_of_syllables += 1
                
            return number_of_syllables
        else:
            return None
            raise LookupError(word + " does not appear to be in the vocabulary...")
    
    def contains_diphthongs(self, word):
        
        diphthongs = ['EY', 'AY', 'AW', 'OY']
        diphthong_phones = []
        
        if self.is_word(word):
            phones = self.phones_without_stress(word)

            for phone in phones:
                if phone in diphthongs:
                    diphthong_phones.append(phone)
        
            return diphthong_phones
        
        else:
            return None
            raise LookupError(word + " does not appear to be in the vocabulary...")

    def character_length(self, word):
        
        characters = list(word)
        alpha_count = 0
        
        for character in characters:
            if character.isalpha():
                alpha_count += 1
            else:
                continue
        
        return alpha_count
            
    def phone_length(self, word):
        if self.is_word(word):
            phones = self.phones_with_stress(word)
            return len(phones)
        else:
            return None
            raise LookupError(word + " does not appear to be in the vocabulary...")
    
    def phones_with_stress(self, word):
        if self.is_word(word):
            return self.vocabulary[word.lower()]
        else:
            return None
            raise LookupError(word + " does not appear to be in the vocabulary...")
    
    def phones_without_stress(self, word):
        phones = self.phones_with_stress(word)
        phones_without_stress = []
        
        if self.is_word(word):
            for phone in phones:
                if any(x.isdigit() for x in phone):
                    phones_without_stress.append(phone[:2])
                else:
                    phones_without_stress.append(phone)
        
            return phones_without_stress
        else:
            return None
            raise LookupError(word + " does not appear to be in the vocabulary...")
    
    def feature_set(self, word):
        phones = self.phones_without_stress(word)
        feature_set = []
        
        if self.is_word(word):
            for phone in phones:
                feature_set.append(self.features[phone])
        
            return feature_set
        else:
            return None
            raise LookupError(word + " does not appear to be in the vocabulary...")
    
    def match(self, word_features = [], phone_features = [], mode = 'CONTAINS', frequency = 'ALL'):
        '''
        Word-level features such as character or phone length, number of syllables, etc.
        can be queried using using a dictionary, e.g.:
        
        {
        'SYLLABLES': 3,
        'CHARACTERS': [6, 10]
        }
        
        This query will return a list of words containing exactly 3 syllables and between 
        6 and 10 characters. Word Feature keys include the following keywords:
        'SYLLABLES' (int or list of ints), 'CHARACTERS' (int or list of ints), 
        'PHONEMES' (int or list of ints), 'CONTAINS_DIPHTHONG' (boolean).
        
        Pattern queries are accepted as lists of dictionaries using the phone-features variable, 
        as in a simplified SpaCy format:
        
        [
        {'FEATURE_A': value_a, 'FEATURE_B': value_b, ...},
        {'FEATURE_C': value_c, 'FEATURE_D': value_d, ...},
        ...
        ]
    
        • Each dictionary corresponds to a single phoneme. 
        • The order of the dictionaries corresponds to the order of the phonemes.
        • The ordering is currently only consecutive. 
        • Use empty dictionaries to match any phoneme.
        • Ranges of values can be queried by placing the extremes in brackets, e.g., [0.0, 0.4].
        • If diphthongs are allowed, singular values will be checked to see whether they fall
          within the range, and ranged values will be checked for overlap.
    
        Example:
    
        [
        {'TYPE': 'C', 'STOP': 1},
        {'TYPE': 'V', 'HEIGHT': [0.6, 1.0]}
        ]
    
        This pattern will match any word containing a stop-consonant (e.g., 'D') immediately
        followed by any mid-high vowel (e.g., 'AH').
        '''
        modes = ['STARTS_WITH', 'ENDS_WITH', 'CONTAINS']
        
        frequencies = ['ALL', 'COMMON_WORDS', 'COMMON_LEMMAS']
        
        # There are three types of lists included.
        # (1) The CMU phonetic dictionary from which both the vocabulary and phonemes are derived.
        #     This includes the most words, including alternate pronunciations, at 135k tokens.
        # (2) A common wordlist including word forms derived from the COCA 60k highest frequency
        #     words sample. The wordlist was pruned to include only words also found in the CMU dictionary,
        #     and includes 5027 tokens. More words, which include word forms, but smaller unique vocabulary.
        # (3) A common wordlist including word lemmas derived from the COCA 60k highest frequency lemmas, and
        #     using the same method of pruning. There are 4369 tokens. Larger unique vocabulary, but only lemmas.
        
        if frequency == 'ALL':
            results = [*self.vocabulary]
        if frequency == 'COMMON_WORDS':
            with open('data/commonwords.txt') as f_in:
                results = [line.strip().lower() for line in f_in.readlines()]
            f_in.close()
        if frequency == 'COMMON_LEMMAS':
            with open('data/commonlemmas.txt') as f_in:
                results = [line.strip().lower() for line in f_in.readlines()]
            f_in.close()
        if frequency not in frequencies:
            raise ValueError("Invalid frequency. Please choose from 'ALL', 'COMMON_WORDS', and 'COMMON_LEMMAS'.")
        
        if mode not in modes:
            raise ValueError("Invalid mode. Please choose from 'STARTS_WITH', 'ENDS_WITH', and 'CONTAINS'.")
        
        # Do the easy part first: get results that satisfy the specified word-level features.
        if len(word_features) > 0:
            
            if 'SYLLABLES' in word_features:
                
                syllables = word_features['SYLLABLES']
                
                if isinstance(syllables, int):
                    results = [word for word in results if self.number_of_syllables(word) == syllables]
                    
                elif isinstance(syllables, list):
                    results = [word for word in results if self.number_of_syllables(word) in range(syllables[0], syllables[1])]
                
            if 'CHARACTERS' in word_features:
                characters = word_features['CHARACTERS']
                
                if isinstance(characters, int):
                    results = [word for word in results if self.character_length(word) == characters]
                    
                elif isinstance(characters, list):
                    results = [word for word in results if self.character_length(word) in range(characters[0], characters[1])]
                
            if 'PHONEMES' in word_features:
                phonemes = word_features['PHONEMES']
                
                if isinstance(phonemes, int):
                    results = [word for word in results if self.phone_length(word) == phonemes]
                    
                elif isinstance(phonemes, list):
                    results = [word for word in results if self.phone_length(word) in range(phonemes[0], phonemes[1])]
                    
            if 'CONTAINS_DIPHTHONG' in word_features: # Only use if it matters.
                diphthong = bool(word_features['CONTAINS_DIPHTHONG'])
                
                if diphthong == True:
                    results = [word for word in results if len(self.contains_diphthongs(word)) > 0]
                
                elif diphthong == False:
                    results = [word for word in results if len(self.contains_diphthongs(word)) == 0]
                    
        
        # phone_features is a list of dictionaries.
        # Each dictionary contains 0 or more features.
        # Each feature value might be a float, list of floats, NoneType, or list of NoneTypes.
        # Each feature set corresponds to a single phoneme.
        # Each feature set is positionally significant.
        
        def compare_features(word_features, phone_features):
            
            match = True
                
            if len(word_features) >= len(phone_features):
                    
                for i in range(0, len(phone_features)):
                        
                    word_phoneme = word_features[i]
                    ptrn_phoneme = phone_features[i]
                        
                    if len(ptrn_phoneme) == 0: # Allow empty feature sets to match any phoneme.
                        continue
                            
                    for feature in ptrn_phoneme:
                                
                        word_value = word_phoneme[feature]
                        ptrn_value = ptrn_phoneme[feature]
                                
                        # First, compare singular values of the same type.
                        if isinstance(ptrn_value, str):
                            if word_value == ptrn_value:
                                continue
                            else:
                                match = False
                                break
                                        
                        if isinstance(ptrn_value, float) and isinstance(word_value, float):
                            if ptrn_value == word_value:
                                continue
                            else:
                                match = False
                                break
                                        
                        if ptrn_value == None and word_value == None:
                                continue
                                        
                        # Second, compare singular word_values to list ptrn_values.
                        if isinstance(ptrn_value, list) and not isinstance(word_value, list):            
                            if isinstance(ptrn_value[0], float) and isinstance(word_value, float):
                                if ptrn_value[0] <= word_value <= ptrn_value[1]:
                                    continue
                                else:
                                    match = False
                                    break
                                            
                            if ptrn_value[0] == None and word_value == None:
                                continue
                                    
                            else:
                                match = False
                                break
                                
                        # Third, compare singular ptrn_values to list word_Values.
                        if isinstance(word_value, list) and not isinstance(ptrn_value, list):         
                            if isinstance(word_value[0], float) and isinstance(ptrn_value, float):
                                if word_value[0]<= ptrn_value <= word_value[1]:
                                    continue
                                else:
                                    match = False
                                    break
                                            
                            if ptrn_value == None and word_value[0] == None:
                                continue
                                        
                            else:
                                match = False
                                break
                                
                        # Finally, compare lists to lists.
                        if isinstance(ptrn_value, list) and isinstance(word_value, list):
                            if ptrn_value[0] == None and word_value[0] == None:
                                continue
                            else:
                                x_min = min(ptrn_value)
                                y_min = min(word_value)
                                x_max = max(ptrn_value)
                                y_max = max(word_value)
                                        
                                if x_min <= y_max and y_min <= x_max:
                                    continue
                                else:
                                    match = False
                                    break
                            
                        else:
                            match = False
                            break
                            
            else:
                match = False
            return match
        
        def starts_with(word, phone_features):
            
            word_features = self.feature_set(word) # list of dictionaries
            
            return compare_features(word_features, phone_features)
        
        def ends_with(word, phone_features):
            
            word_features = self.feature_set(word)
            word_features.reverse()
            
            phone_features.reverse()
            
            return compare_features(word_features, phone_features)
        
        def contains(word, phone_features):
            
            word_features = self.feature_set(word)
            
            match = False
            
            while len(word_features) >= len(phone_features) and match == False:
                if compare_features(word_features, phone_features) == False:
                    word_features.pop(0)
                else:
                    match = True
            
            return match
        
        if len(phone_features) > 0:
            
            if mode == 'STARTS_WITH':
                
                results = [word for word in results if starts_with(word, phone_features) == True]
                
            elif mode == 'ENDS_WITH':
                
                results = [word for word in results if ends_with(word, phone_features) == True]
                
            elif mode == 'CONTAINS':
                
                results = [word for word in results if contains(word, phone_features) == True]
        
        return results
