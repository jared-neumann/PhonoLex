from distutils.core import setup

setup(
  name = 'phonolex',
  packages = ['phonolex'],
  package_dir = {'phonolex': 'src/phonolex'},
  package_data={'phonolex': ['data/cmu.json', 'data/features.json', 'data/commonwords.txt', 'data/commonlemma.txt']},
  version = '0.0.1-alpha',  license='gplv3',
  description = 'This is a small package to describe the phonology of words and find matches for word features and/or phonological patterns.',
  author = 'Jared Neumann',
  author_email = 'janeuman@iu.edu',
  url = 'https://github.com/janeumanIU/PhonoLex',
  keywords = ['phonology', 'pattern', 'speech language pathology', 'linguistics', 'phonetics'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3'
  ]
)
