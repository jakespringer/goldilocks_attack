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

6. To get results, run `automate.py --topk [topk] --dictionary {l2|frequency|random} --type {same|different|single}`
and look in the generated `data/results` folder. See instructions in the `./python` section for further details.

## `./code2seq`

The implementation of code2seq with modifications to the preprocessing script `preprocess2.sh`, 
along with a precompiled version of JavaExtractor.

## `./bash`

* `download-model-and-dataset.sh` is a script to download and automatically install the java-large model
and the java-small dataset so that they are ready to be attacked.

## `./java`

The implementation of RenameVariable, a tool that uses JavaParser to rename local variables for the attack.

## `./python`

* `automate.py --topk [topk] --dictionary {l2|frequency|random} --type {same|different|single}` runs
the automate script to generate a perturbation using the l2, frequency, or random dictionary (`--dictionary`)
with a top-k parameter of `topk` (integer). The attacks use a concatenation strategy of either single, 5-diff, or 5-same
(`--type`).
* `{l2|frequency|all}_dictionary.py [topk]` generates a vocabulary of the topk subtokens by the given metric.
* `attack_config.py` has a few parameters to specify location of the code2seq model, input dataset, and output files.
* `filter_has_local_variables.py [c2s file]` generates a file in c2s format from the c2s file input of only methods 
that contain local variables.
* `perturb_dataset.py [output directory] [vocabulary file] [subtoken concatenation strategy]` calls the RenameVariable 
tool to perturb the dataset specified in `attack_config.py` with tokens from vocabulary file that are concatenated with
concatenation strategy.
* `modified_model.py` has an implementation of the code2seq model that exposes important internals.

## `./data`

Miscellaneous data, including input and output files.
