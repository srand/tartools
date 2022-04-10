from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
name = "tartools"
exec(open('tartools/version.py').read())


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=name,
    version=__version__,
    description='Tools to diff and patch tar archives and filesystem trees',
    long_description=long_description,
    url="https://github.com/srand/tartools",
    author="Robert Andersson",
    author_email="srand@github.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Topic :: System :: Archiving",
    ],
    keywords=[
        "bsdiff",
        "tar",
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    dependency_links=[],
    entry_points={
        'console_scripts': [
            'tarapply=tartools.cmds.tarapply:main',
            'tardiff=tartools.cmds.tardiff:main',
            'tarsum=tartools.cmds.tarsum:main',
        ],
    },
    install_requires=[
        "bsdiff4",
    ],
    extras_require={
        "test": ["behave"],
    },
)
