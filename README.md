# Neutrino-flare significance
Estimate the significance of the three accretion flares that are coincident with an IceCube alert, reproducing the analysis of van Velzen et al. [arXiv:2111.09391](https://arxiv.org/abs/2111.09391). 


## Requirements 
- `scipy`   install with pip
- `astropy` install with pip
- `k3match` install from [repo](https://github.com/pschella/k3match)
- `sjoert` install from [repo](https://github.com/sjoertvv/sjoert)

## How to 
```python3 run_TS.py``` 

This gets you straight to the final result, an estimate of the significance with the most sensible settings of the likelihood ratio test. Executing this should take a few minutes on a single core (a few GB of working memory needed). 

To explore the intermediate steps, consider running the scripts that make the figures: `plot_skymaps.py` and `plot_PDFs.py`.

To change the settings of the likelihood method, edit the dictionary in `load_data.py` (more documentation provided in this file).  

### Lancel?
The nicknames of three flares with a potential neutrino counterpart are: 
- AT2019dsg: Bran Stark
- AT2019fdr: Tywin Lannister
- AT2019aalc: Lancel Lannister
