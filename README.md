# Neutrino-flare significance
Estimate the significance of the three accretion flares that are coincident with an IceCube alert, reproducing the analysis of van Velzen et al. [arXiv:2111.09391](https://arxiv.org/abs/2111.09391).

## Installation

You can install this package with just two steps:

`git clone https://github.com/sjoertvv/HelloLancel.git`

`pip install -e HelloLancel`

This will install the package, and all the associated dependencies.

## How to 
### Reproduce the final result
```python hellolancel/run_TS.py``` 

This gets you straight to the final result, an estimate of the significance with the most sensible settings of the likelihood ratio test. Executing this should take a few minutes on a single core (a few GB of working memory needed). 

### Dig deeper
To explore the intermediate steps, consider running the scripts that make the figures: `hellolancel/plot_skymaps.py` and `hellolancel/plot_PDFs.py`.

To change the settings of the likelihood method, edit the dictionary in `hellolancel/settings.py` (further documentation provided inside this file).  

### MC-free
It can be insightful to look at the signififance (3.2 sigma) obtained solely from the low area denisity of ZTF flares with large dust echoes. This is computed in `hellolancel/simple_significance.py`. 

## Lancel?
The nicknames of three flares with a potential neutrino counterpart are: 
- AT2019dsg: Bran Stark
- AT2019fdr: Tywin Lannister
- AT2019aalc: Lancel Lannister
