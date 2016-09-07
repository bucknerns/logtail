import os
from setuptools import setup, find_packages

# Establish a consistent base directory relative to the setup.py file
os.chdir(os.path.abspath(os.path.dirname(__file__)))

setup(
    name="logtail",
    version="0.0.6",
    description="Package for tailing logs and viewing in editor",
    long_description=open("README.md").read(),
    author="Nathan Buckner",
    author_email="nathan.buckner@rackspace.com",
    url="http://github.com/bucknerns",
    license=open("LICENSE").read(),
    packages=find_packages(),
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: Other/Proprietary License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"),
    entry_points={
        "console_scripts":
        ["logtail = logtail.logtail:main",
         "editlatest = logtail.logtail:editlatest"]})
