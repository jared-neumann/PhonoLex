import json, os

def load_data(
    vocabulary_path = '/data/cmu.json',
    commonwords_path = '/data/commonwords.txt',
    commonlemmas_path = '/data/commonlemmas.txt',
    features_path = '/data/features.json'
    ):

    parent = os.path.dirname(os.path.abspath(__file__))

    with open(parent + vocabulary_path) as in_file:
        vocabulary = json.load(in_file)
    in_file.close()

    with open(parent + features_path) as in_file:
        features = json.load(in_file)
    in_file.close()

    with open(parent + commonwords_path) as in_file:
        commonwords = [word.strip() for word in in_file]
    in_file.close()

    with open(parent + commonlemmas_path) as in_file:
        commonlemmas = [word.strip() for word in in_file]
    in_file.close()

    return {
        'vocabulary': vocabulary,
        'commonwords': commonwords,
        'commonlemmas': commonlemmas,
        'features': features
        }

class Phonology():

    # Use loaded data.
    def __init__(self, data = load_data()):
        self.vocabulary = data['vocabulary']
        self.commonwords = data['commonwords']
        self.commonlemmas = data['commonlemmas']
        self.features = data['features']

    def describe(self, word):
        return {
            'word': word,
            'is word': self.is_word(word),
            'number of syllables': self.number_of_syllables(word),
            'contains diphthongs': self.contains_diphthongs(word),
            'character length': self.character_length(word),
            'phoneme length': self.phone_length(word),
            'phonemes': self.phones_without_stress(word),
            'stress': self.phones_with_stress(word),
            'features': self.feature_set(word)
            }

    # Check if a given word is in the vocabulary.
    # TO-DO: Add options for other wordlists.
    def is_word(self, word):
        if word.lower() in self.vocabulary:
            return True
        else:
            return False

    # Get the number of syllables in a given word
    # by counting the number of numbers appended to
    # vowels in the data.
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

    # Check if word contains any diphthong
    # by comparing phonemes against a list of diphthongs.
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

    # Count the number of characters in the word.
    def character_length(self, word):
        
        characters = list(word)
        alpha_count = 0
        
        for character in characters:
            if character.isalpha():
                alpha_count += 1
            else:
                continue
        
        return alpha_count

    # Count the number of phonemes in the word.
    def phone_length(self, word):
        if self.is_word(word):
            phones = self.phones_with_stress(word)
            return len(phones)
        else:
            return None

    # Retrieve the phonemes for a given word without modification.
    def phones_with_stress(self, word):
        if self.is_word(word):
            return self.vocabulary[word.lower()]
        else:
            return None

    # Retrieve the phonemes for a given word with stress markers removed.
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

    # Construct the feature set using the separate features files
    # and looking up each phoneme in the word.
    def feature_set(self, word):
        phones = self.phones_without_stress(word)
        feature_set = []
        
        if self.is_word(word):
            for phone in phones:
                feature_set.append(self.features[phone])
        
            return feature_set
        else:
            return None

    # Core function to match features and feature patterns.            
    def match(self, word_features = {}, phone_features = [], mode = 'CONTAINS', frequency = 'ALL'):
        
        modes = ['STARTS_WITH', 'ENDS_WITH', 'CONTAINS'] # Define the variable options.
        frequencies = ['ALL', 'COMMON_WORDS', 'COMMON_LEMMAS']

        # For a description of the wordlists, see the README.
        # Set the vocabulary to one of the given wordlists.
        # Results are obtained by pruning the vocabulary.
        # TO-DO: Results are rewritten for every condition.
        # Efficiency probably needs to be improved eventually.
        if frequency == 'ALL':
            results = [*self.vocabulary]
        elif frequency == 'COMMON_WORDS':
            results = self.commonwords
        elif frequency == 'COMMON_LEMMAS':
            results = self.commonlemmas
        else:
            raise ValueError("Invalid frequency. Please choose from 'ALL', 'COMMON_WORDS', and 'COMMON_LEMMAS'.")
        
        # Do the easy part first: get results that satisfy the specified word-level features.
        # For a description of the feature and pattern formats, see the README.
        if len(word_features) > 0:
            
            if 'SYLLABLES' in word_features:
                
                syllables = word_features['SYLLABLES']

                # Because there are multiple data types we can compare,
                # check each type and create conditions for comparison.
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

        # Core function for the modes of comparison; same in all cases with
        # different passed variables.
        def compare_features(word_features, phone_features):
            
            match = True # Initialize match to True.
                
            if len(word_features) >= len(phone_features):
                    
                for i in range(0, len(phone_features)):
 
                    word_phoneme = word_features[i] # Compare phoneme features at the same index.
                    ptrn_phoneme = phone_features[i]
                        
                    if len(ptrn_phoneme) == 0: # Allow empty feature sets to match any phoneme.
                        continue
                            
                    for feature in ptrn_phoneme:

                        word_value = word_phoneme[feature] # Compare the same features.
                        ptrn_value = ptrn_phoneme[feature]
                                
                        # First, compare singular values of the same type.
                        if isinstance(ptrn_value, str):
                            if word_value == ptrn_value:
                                continue
                            else:
                                match = False
                                break
                                        
                        elif isinstance(ptrn_value, float) and isinstance(word_value, float):
                            if ptrn_value == word_value:
                                continue
                            else:
                                match = False
                                break
                                        
                        elif ptrn_value == None and word_value == None:
                                continue
                                        
                        # Second, compare singular word_values to list ptrn_values.
                        elif isinstance(ptrn_value, list) and not isinstance(word_value, list):            
                            if isinstance(ptrn_value[0], float) and isinstance(word_value, float):
                                if ptrn_value[0] <= word_value <= ptrn_value[1]:
                                    continue
                                else:
                                    match = False
                                    break
                                            
                            elif ptrn_value[0] == None and word_value == None:
                                continue
                                    
                            else:
                                match = False
                                break
                                
                        # Third, compare singular ptrn_values to list word_Values.
                        elif isinstance(word_value, list) and not isinstance(ptrn_value, list):         
                            if isinstance(word_value[0], float) and isinstance(ptrn_value, float):
                                if word_value[0]<= ptrn_value <= word_value[1]:
                                    continue
                                else:
                                    match = False
                                    break
                                            
                            elif ptrn_value == None and word_value[0] == None:
                                continue
                                        
                            else:
                                match = False
                                break
                                
                        # Finally, compare lists to lists.
                        elif isinstance(ptrn_value, list) and isinstance(word_value, list):
                            if ptrn_value[0] == None and word_value[0] == None:
                                continue
                            else: # Check overlap of values in lists.
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
            
            # compare_features() starts at index = 0 already,
            # so no interesting modifications are necessary.
            word_features = self.feature_set(word)
            
            return compare_features(word_features, phone_features)
        
        def ends_with(word, phone_features):
            
            # we need to reverse both the phonemes and the features/patterns
            # in order to get the indices in the right order to check a match
            # from the end of the word.
            word_features = self.feature_set(word)
            word_features.reverse()
            
            phone_features.reverse()
            
            return compare_features(word_features, phone_features)
        
        def contains(word, phone_features):
            
            # This is the most difficult computationally.
            # Not sure how to improve it yet.
            # Check if a pattern matches starting from index = 0,
            # if not, pop that first index and start over.
            word_features = self.feature_set(word)
            
            match = False
            
            while len(word_features) >= len(phone_features) and match == False:
                if compare_features(word_features, phone_features) == False:
                    word_features.pop(0)
                else:
                    match = True
            
            return match

        # If the user passes a phoneme pattern, find matches according to one of the above modes.
        if len(phone_features) > 0:
            if mode == 'CONTAINS':
                results = [word for word in results if contains(word, phone_features) == True]

            elif mode == 'STARTS_WITH':
                results = [word for word in results if starts_with(word, phone_features) == True]
                
            elif mode == 'ENDS_WITH':
                results = [word for word in results if ends_with(word, phone_features) == True]
                
            else:
                raise ValueError("Invalid mode. Please choose from 'STARTS_WITH', 'ENDS_WITH', and 'CONTAINS'.")
            
        return results       
