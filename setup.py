#!/usr/bin/env python
from setuptools import convert_path, setup, find_packages

version = {}
version_path = convert_path('defisdk/version.py')
with open(version_path) as f:
    exec(f.read(), version)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='defisdk',
    version=version['__version__'],
    author='Alex Bash',
    author_email='alexey@zerion.io',
    description='DeFiSDK.py',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zeriontech/defi-sdk-py',
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.7.4.post0',
        'furl==2.1.3',
        'pysha3==1.0.2',
    ],
    python_requires='>=3.7',
)
