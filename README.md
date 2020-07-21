# code2seq_attack_Jake_Springer
Code2Seq for Jake Springer Summer UROP

This implementation of the Goldilocks attack is split up into a number of 
components. In particular, we have the following:
* `python/modified_model.py` which loads the code2seq model and then exposes
  a number of internals useful for gradient-based attacks.
* `python/{frequency,l2}_dictionary.py`, which generates the perturbation
  dictionaries.
* `java/../RenameVariable.java`, which modifies Java source code with a perturbation
* `python/perturb_dataset.py`, which runs the perturbation code on an entire
  dataset.

To use the attack, you need to do the following:
1. Generate a dictionary for the attack.
2. Perturb a dataset with the dictionary.
3. Preprocess the perturbed dataset (using code2seq's implementation).
4. Run code2seq on the perturbed dataset (using code2seq's implementation).

Examples of command line usage of the libraries (cannot be copied and pasted but is here for reference):
```
python frequency_dictionary.py 10000 > ../data/frequency_dictionary_10000.txt
python perturb_dataset.py ../data/java-small-frequency-10000-same ../data/frequency_dictionary_10000.txt same
```

and then see code2seq for preprocessing the dataset and running the model.



------------------------------------------------

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
