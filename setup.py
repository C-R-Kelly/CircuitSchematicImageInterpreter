# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

if os.path.exists('README.md'):
    long_description = open('README.md').read()
else:
    long_description = '''Software for the digital interpretation of electrical-circuit schematic images.'''

setup(
    name='CircuitSchematicImageInterpreter',
    version='1.0.0',
    author='Charles R. Kelly',
    author_email='CK598@cam.ac.uk',
    license='MIT',
    url='https://github.com/C-R-Kelly/CircuitSchematicImageInterpreter',
    packages=find_packages(),
    description='Software for the digital interpretation of electrical-circuit schematic images.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='',
    install_requires=[
        'pytesseract>=0.3.8',
        'matplotlib>=3.5.0',
        'networkx>=2.6.3',
        'numpy>=1.21.2',
        'pillow>=8.4.0',
        'scikit-image>=0.18.3',
        'scipy>=1.7.3',
        'sympy>=1.13.dev0',
    ],
)
