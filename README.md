# Master's Thesis Project

Code used for experiments in my Master Thesis project that was done in collaboration with NRK:

> Automatic Topic Generation for Broadcasters:
> Usable Metadata from Topic Models on
> Systematically Preprocessed TV Subtitles

`./textPrep` contains the textPrep library as adapted from [textPrep](https://github.com/GU-DataLab/topic-modeling-textPrep). Here, the library has been modified to work for the Norwegian dataset used in the Master Thesis project. The modified version (fork) of textPrep can be found [here](https://github.com/magnurr/topic-modeling-textPrep-Norwegian-subtitles).

## Setup

1. Clone this repo
1. Install python 3.6 or higher
1. Install [iPython kernel](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)
1. Go to this folder on your machine: `cd Master-Thesis-Project`
1. Make sure you are in the Silje branch: `git checkout silje-lda-prosjekt`
1. Install python packages: `pip install -r requirements.txt`
1. Now you should be good! Go to `lda.ipynb`, try to run the code cells and explore for yourself
