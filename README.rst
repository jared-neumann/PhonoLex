========
PhonoLex
========
A small package to describe the phonology of words and find words satisfying word-level features and/or phonological patterns defined by the user.

.. contents:: Table of Contents

Overview
========

Description
-----------

The core functionality of this package is to allow users to define phonological patterns and query lists of words for matches. Word-level features may also be defined, including character and phoneme length, the presence of diphthongs, the number of syllables, and the desired frequency of the word. Phoneme-level features that may be used to define patterns include many standard manners of articulation. There are three modes of matching a pattern: STARTS_WITH, ENDS_WITH, and CONTAINS. Users may also query a particular word to obtain its phonological description. 

Use-Case
--------

The package was initially developed to aid speech-language pathologists in developing phonologically defined word lists for certain therapies. An actual example is given in the 

Data
====
The data folder includes four files: cmu.json, features.json, commonlemmas.txt, and commonwords.txt.

CMU Pronouncing Dictionary
--------------------------
The default wordlist is the Carnegie Mellon University Pronouncing Dictionary [1]_ (cmu.json). The file was compiled into json format with words as keys and lists of phonemes (with stress indicated) as their respective values. It includes approximately 135k English words.

**Vocabulary Example**

+--------+-----+-----+-----+-----+-----+-----+
|        |  0  |  1  |  2  |  3  |  4  |  5  |
+========+=====+=====+=====+=====+=====+=====+
| banana |  B  | AH0 |  N  | AE1 |  N  | AH0 |
+--------+-----+-----+-----+-----+-----+-----+

ARPAbet Feature Sets
--------------------
The features.json file maps the ARPAbet symbols used for phonemes in the CMU Pronouncing Dictionary (as above) to their corresponding articulatory features. These features were derived from the symbol definitions and their correspondence to IPA symbols [2]_. The defined features can be seen in the following example for 'IH':

**Features Example**

+--------------+------+
|FEATURES      | IH   |
+==============+======+
|TYPE          | V    |
+--------------+------+
|HEIGHT        | 0.2  |
+--------------+------+
|DEPTH         | 0.75 |
+--------------+------+
|ROUNDED       | 0    |
+--------------+------+
|RHOTIC        | 1    |
+--------------+------+
|STOP          | None |
+--------------+------+
|VOICE         | None |
+--------------+------+
|BILABIAL      | None |
+--------------+------+
|AFFRICATE     | None |
+--------------+------+
|ALVEOPALATAL  | None |
+--------------+------+
|ALVEOLAR      | None |
+--------------+------+
|FRICATIVE     | None |
+--------------+------+
|DENTAL        | None |
+--------------+------+
|LABIODENTAL   | None |
+--------------+------+
|VELAR         | None |
+--------------+------+
|LATERAL       | 0    |
+--------------+------+
|POSTALVEOLAR  | None |
+--------------+------+
|NASAL         | None |
+--------------+------+
|LABIOVELAR    | None |
+--------------+------+
|PALATAL       | None |
+--------------+------+
|GLIDE         | None |
+--------------+------+
|GLOTTAL       | None |
+--------------+------+

The values may have the following data types: *string* (for TYPE, i.e., vowel or consonant), *float* (for all numerical values, even those that are binary), *None* (for the cases in which a feature is not applicable/possible), and *list* (for ranges of values as in the case of diphthongs or search queries).

Vowel Chart
___________

It may be useful to see how the vowels were plotted on the height/depth continuum. A fuller reference will be provided for all phoneme features, but for the time being refer to the following graph.

.. image:: src/phonolex/info/vowels.png

COCA Common Words and Lemmas
----------------------------

**Common Words**

A list containing 5027 of the most common words in English is included in commonwords.txt. The list was derived from the Corpus of Contemporary American English (COCA) 2020 data [3]_. The original sample of common words was obtained from www.wordfrequency.info and cross-referenced with the CMU dictionary to ensure queries were always possible. Duplicates were also removed. The trade-off of calling this wordlist is that there are more tokens, but a smaller unique vocabulary, than in the commonlemmas.txt file.

**Common Lemmas**

Similarly, a list of 4369 of the most common lemmas in English was derived from the same source and in the same manner. The trade-off here is the reverse: a smaller set of tokens, but a larger unique vocabulary.

Usage
=====

Currently there is only the core Phonology class.

Initializing
------------
To initialize the Phonology class:

::

  from phonolex.phonology import Phonology
  ph = Phonology()

Phonological data for a particular word can be accessed directly by utilizing any of the functions included in the class. However, they are all collected by the describe() function:

::

  ph.describe('banana')

Returns a dictionary containing the following information:

+----------------------+
|Word-Level Features   |
+============+=========+
| word       | banana  |
+------------+---------+
| is_word    | True    |
+------------+---------+
| syllables  | 3       |
+------------+---------+
| diphthongs | []      |
+------------+---------+
| characters | 6       |
+------------+---------+
| phonemes   | 6       |
+------------+---------+

|

+-------------------------------------------------------+
|Phoneme-Level Features                                 |
+=============+======+======+======+======+======+======+
|PHONEMES     |   B  | AH   | N    | AE   |  N   |  AH  |
+-------------+------+------+------+------+------+------+
|STRESS       |   B  | AH0  |  N   | AE1  |  N   | AH0  |
+-------------+------+------+------+------+------+------+
|TYPE         |   C  |  V   | C    | V    | C    | V    |
+-------------+------+------+------+------+------+------+
|HEIGHT       | None |0.6   | None | 0.8  | None | 0.6  |
+-------------+------+------+------+------+------+------+
|DEPTH        | None |  0   | None |  1   | None |  0   |
+-------------+------+------+------+------+------+------+
|ROUNDED      | None |  0   | None |  0   | None |  0   |
+-------------+------+------+------+------+------+------+
|RHOTIC       |   0  |  0   | 0    |  0   | 0    | 0    |
+-------------+------+------+------+------+------+------+
|STOP         |   1  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|VOICE        |   1  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|BILABIAL     |   1  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|AFFRICATE    |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|ALVEOPALATAL |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|ALVEOLAR     |   0  |None  | 1    | None |  1   | None |
+-------------+------+------+------+------+------+------+
|FRICATIVE    |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|DENTAL       |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|LABIODENTAL  |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|VELAR        |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|LATERAL      |   0  |  0   | 0    | 0    | 0    | 0    |
+-------------+------+------+------+------+------+------+
|POSTALVEOLAR |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|NASAL        |   0  |None  | 1    | None |  1   | None |
+-------------+------+------+------+------+------+------+
|LABIOVELAR   |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|PALATAL      |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|GLIDE        |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+
|GLOTTAL      |   0  |None  | 0    | None |  0   | None |
+-------------+------+------+------+------+------+------+

*CAUTION*: Currently, the describe() function only returns the key that is passed, so does not include alternate pronunciations (indicated with an appended numeral in parentheses, e.g., (2)).

Functions
---------
The functions that generate the above information can used independently, otherwise investigate the output of the *describe()* function to find the keys relevant to your purpose. Full documentation is in the works.

The core functionality of the Phonology class is pattern-matching. To query the data for particular patterns, use the *match()* function:

::
  
  ph.match(word_features = {}, phone_features = [], mode = 'CONTAINS', frequency = 'ALL')

**word_features**

Word-level features are specified using a dictionary of features. The possible features are 'SYLLABLES', 'CHARACTERS', 'PHONEMES', 'CONTAINS_DIPHTHONG'. The first three require integer values, while the last requires a boolean. Note: 'CONTAINS_DIPHTHONG' should only be used if it matters whether the results contain diphthongs. False will result in no matches with diphthongs and True will result in all matches with diphthongs.

*word_features example*

::

  word_features = {'SYLLABLES': 3, 'CHARACTERS': [5, 10], 'CONTAINS_DIPHTHONG': False}

Notice that the integers values could also be lists of two integers values. This will define a range with a min and max. That means this query will only return words with anywhere from 5 to 10 characters.

**phone_features**

Phoneme-level features are specified using a *list* of dictionaries containing features. The possible features are all those included in the above table containing the manners of articulation with the indicated data types. The list is positional, so the order matters. The pattern will be matched in the order it occurs in the word.

*phone_features example*

::

  phone_features = [
  {'TYPE': 'C', 'STOP': 1.0}, 
  {'TYPE': 'V', 'HEIGHT': [0.6, 1.0]}
  ]

This pattern will match any word containing a stop-consonant (e.g., 'D') immediately followed by any mid-high vowel (e.g., 'AH'). Also note that empty dictionaries can be added into a position in order to match anything.

**mode**

Mode allows the user to indicate whether a pattern should be matched anywhere (default), from the beginning of the word, or at the end of the word. Options are 'CONTAINS', 'STARTS_WITH', and 'ENDS_WITH'. They each use the same comparison function, but manipulate a word's phoneme list to get the appropriate results.

**frequency**

Frequency allows the user to indicate whether the entire CMU Pronouncing Dictionary should be searched or one of the smaller wordlists. Options are 'ALL' (CMU), 'COMMON_WORDS' (common words with word forms), and 'COMMON_LEMMAS' (common words in the base form). The benefits of each are given above.

Examples
--------
The following are example queries. The first two have been contrived. The third is from the use-case mentioned above.

**Example 1**

::

  word_features = {'SYLLABLES': 3, 'CHARACTERS': [5, 10], 'CONTAINS_DIPHTHONG': False}

  phone_features = [
  {'TYPE': 'C', 'STOP': 1.0}, 
  {'TYPE': 'V', 'HEIGHT': [0.6, 1.0]}
  ]
  
  ph.match(word_features, phone_features, mode = 'STARTS_WITH', frequency = 'COMMON_WORDS')

This query returns a list containing 114 items:
['together', 'company', 'possible', 'policy', 'personal', 'companies', 'position', 'continue', 'director', 'potential', ...]

The same query using the CMU vocabulary returns 4741 results. Using the common lemmas wordlist, there are 107 results.

**Example 2**

::

  word_features = {'SYLLABLES': [1,2], 'CHARACTERS': [4,6], 'CONTAINS_DIPHTHONG': False}

  phone_features = [
  {'TYPE': 'C', 'ALVEOLAR': 1.0, 'STOP': 1.0},
  {},
  {'TYPE': 'V', 'DEPTH': [0.0,0.4]},
  {'TYPE': 'C', 'NASAL': 1.0}
  ]

  ph.match(word_features, phone_features, mode = 'CONTAINS', frequency = 'ALL')

This query returns a list of 18 items: ['drawn', 'drone', 'drum', 'drumm', 'drums', 'drunk', 'dwan', 'strom', 'strum', 'tian', 'traum', 'tromp', 'tron', 'trone', 'troon', 'trump', 'trunk', 'twang'].

The same query using the common words list returns 3 results: ['trump', 'drawn', 'drunk']. Using the common lemmas list, 3 different results: ['drunk', 'trunk', 'drum'].

**Example 3**

::

  word_features = {'SYLLABLES': 2, 'CONTAINS_DIPHTHONG': False}

  phone_features = [
  {'TYPE': 'C', 'VOICE': 0.0, 'ALVEOLAR': 1.0, 'STOP': 1.0}, # /t/
  {'TYPE': 'V', 'DEPTH': 1.0} # Front vowels
  ]

  ph.match(word_features, phone_features, mode = 'STARTS_WITH', frequency = 'COMMON_LEMMAS')

This query returns a list of 18 items: ['teacher', 'tv', 'technique', 'teaching', 'talent', 'teaspoon', 'tension', 'testing', 'terror', 'tactic', 'temple', 'tackle', 't-shirt', 'tablet', 'tennis', 'tender', 'tattoo', 'textbook'].

References
==========
.. [1] Carnegie Mellon University Pronouncing Dictionary. http://www.speech.cs.cmu.edu/cgi-bin/cmudict.
.. [2] ARPABET Reference. https://en.wikipedia.org/wiki/ARPABET.
.. [3] COCA 2020 Word Frequency Data. https://www.wordfrequency.info/samples.asp.
