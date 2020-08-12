# Implementation of Goldilocks attack
From [add link to paper here]

## Overview

This is an implementation of the Goldilocks attack on code2seq. The attack
is performed in a number of steps, but the automation script should do the
heavy lifting of putting everything together. 

## Installation

1. To install this attack, you will first need to install Python 3.5+ and all of the
dependencies listed in `python/requirements.txt`.

2. You will need an installation of the Java Runtime Environment (version 8+). I
recommend `sudo apt install default-jre`.

3. This repository includes a modified implementation of code2seq (original can be found at 
https://github.com/tech-srl/code2seq). Add our implementation of code2seq to your PYTHONPATH.

4. The file `python/attack_config.py` includes a few parameters that can be modified to 
configure the attack, including the dataset to perturb and the code2seq model to use. Take a
look at this file and determine the appropriate configuration. To reproduce the java-large
results of the paper, you do not have to change this file.

5. If you wish to reproduce the java-large results of the paper, you can run the script
`bash/download-model-and-dataset.sh` and follow the instructions. Run this script from 
the bash directory.

6. To get results, run `automate.py --topk [topk] --dictionary [l2|frequency|random] --type [same|different|single]`
and look in the generated `data/results` folder. See instructions in the `./python` section for further details.

## `./code2seq`

## `./bash`

## `./java`

## `./python`

## `./data`
