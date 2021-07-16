from distutils.core import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
  name = 'phonolex',
  packages = ['phonolex'],
  package_dir = {'phonolex': 'src/phonolex'},
  package_data={'phonolex': ['data/cmu.json', 'data/features.json', 'data/commonwords.txt', 'data/commonlemmas.txt']},
  version = '0.0.2-beta.post1',  license='gplv3',
  description = 'This is a small package to describe the phonology of words and find matches for word features and/or phonological patterns.',
  author = 'Jared Neumann',
  author_email = 'janeuman@iu.edu',
  url = 'https://github.com/janeumanIU/PhonoLex',
  keywords = ['phonology', 'pattern matching', 'speech language pathology', 'linguistics', 'phonetics'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3'
  ],
  long_description = long_description,
  long_description_content_type = 'x-rst'
)
