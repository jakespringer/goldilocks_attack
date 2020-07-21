# Implementation of Goldilocks attack
Jacob Springer Summer UROP

This is an implementation of the Goldilocks attack on code2seq. The attack
is performed in a number of steps, but the automation script should do the
heavy lifting of putting everything together. The hard part is installing 
everything appropriately.

## Installation

1. To install this attack, you will first need to install Python 3.5+ and all of the
dependencies listed in `python/requirements.txt`.

2. You will need an installation of the Java Runtime Environment (version 8+). I
recommend `sudo apt install default-jre`.

3. Next, you will need to download and install code2seq (https://github.com/tech-srl/code2seq).
You will need to download (or create) a trained model and a dataset to perturb. I recommend
the model that code2seq provides for download and the java-small dataset, also provided by 
code2seq. Add code2seq to your PYTHONPATH.

4. Copy the file `bash/preprocess2.sh` into your code2seq installation directory; it is used by
this code, but needs to be located in that directory.

5. The files in the `python` directory,`automate.py`, `frequency_dictionary.py`, `l2_dictionary.py`, 
`perturb_dataset.py` have a number of parameters that are labeled for change. Follow the
instructions in each file.

6. To get results, run `automate.py --topk [topk] --dictionary [l2|frequency]`
