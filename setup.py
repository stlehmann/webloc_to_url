import os
import sys
import ast
import re
from setuptools import setup
from setuptools.command.test import test as TestCommand


setup(
    name='webloc_to_url',
    version='0.0.1',
    packages=[],
    license='MIT',
    author='Stefan Lehmann',
    author_email='stlm@posteo.de',
    scripts=['webloc_to_url.py'],
    install_requires=['validators', 'click'],
    entry_points={
        'console_scripts': [
            'webloc_to_url=webloc_to_url:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ]
)