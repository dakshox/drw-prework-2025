# setup.py
from setuptools import setup, find_packages

setup(
    name="drw-prework-2025",          # you can choose any distribution name
    version="0.1.0",
    packages=find_packages(),  # automatically finds cmds/
    install_requires=[         # any runtime deps your modules need
        # e.g. "numpy>=1.24",
    ],
)
