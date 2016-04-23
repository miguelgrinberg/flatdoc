import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as fp:
    long_description = fp.read()

setup(
    name='flatdoc',
    description='Docstring flat documentation generator',
    long_description=long_description,
    version='0.1.0',
    author='Miguel Grinberg',
    author_email='miguelgrinberg50@gmail.com',
    url='https://github.com/miguelgrinberg/flatdoc',
    license='MIT',
    py_modules=['flatdoc'],
    install_requires=['qualname'],
    entry_points={
        'console_scripts': [
            'flatdoc = flatdoc:main',
        ],
    },
    test_suite='test_flatdoc',
    tests_require=['coverage', 'flake8'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
