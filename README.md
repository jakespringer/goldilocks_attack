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
