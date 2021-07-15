from setuptools import setup, find_packages


with open('README.txt', mode = 'r', encoding = 'utf8') as f:
    readme = f.read()

with open('LICENSE.txt', mode = 'r', encoding = 'utf8') as f:
    license = f.read()

with open('requirements.txt', mode = 'r', encoding = 'utf8') as f:
    requirements = f.read()

setup(
    
    name = 'phonolex',
    version = '0.1.0',
    description = 'Package for describing the phonology of words and finding matches for phonological patterns.',
    long_description = readme,
    author = 'Jared Neumann',
    author_email = 'janeuman@iu.edu',
    requirements = requirements,
    license = license,
    packages = find_packages()
    
)
