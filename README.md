# Assignment 4 Evaluating FairSHAP

[Download ZIP](https://github.com/Achiee7/DW-Assignment-4-FairSHAP/archive/refs/heads/main.zip)
· [Read the notebook](Assignment%204%20FairSHAP.ipynb)

This notebook evaluates the method in
[Zhu, Bian and You (2026)](https://proceedings.mlr.press/v300/zhu26b.html) on
German Credit, COMPAS and Adult. It includes the downloaded datasets, an
explained implementation, completed results and a comparison with the paper.

## Download and run

1. Install **Python 3.12** if it is not already available.
2. On this GitHub page, choose **Code → Download ZIP** and extract the ZIP.
3. Open the extracted project folder in a notebook app, such as **VS Code with
   Jupyter support** or **JupyterLab**. Open `Assignment 4 FairSHAP.ipynb`.
4. Select a **Python 3.12** kernel and choose **Run All**.

**No terminal commands or manual package installation are needed.** The first
cell installs the pinned packages into the selected Python environment, then
the remaining cells run the experiment. An internet connection is needed for
that first setup. A notebook app is needed to open and execute `.ipynb` files;
Python by itself does not provide that interface.

The datasets and saved outputs are included, so the notebook can also be read
without rerunning. Once package setup is complete, the experiment took one to
two minutes on the workstation. Running again overwrites the local results and
notebook outputs; the downloaded ZIP and the GitHub files remain available.

## What the experiment does

The notebook first measures fairness in the original labels, before fitting
any classifier. An ordinary XGBoost model and a model retrained after FairSHAP
are then compared on exactly the same untouched test set. The reported
measures are demographic-parity difference, disparate impact ratio,
neighbour consistency, accuracy and discriminative risk.

The full implementation is inside the notebook. It does not need a cloned copy
of the authors' repository.

## Fixed settings

- All 1,000 German Credit, 7,214 COMPAS and 32,561 Adult records; no subsampling.
- Joint label/sex stratified 80/20 split, seed 42.
- XGBoost: 100 trees, maximum depth 6, learning rate 0.3, histogram trees,
  four CPU threads; 0.5 decision threshold.
- Each training row is matched to its nearest opposite-sex row with the same
  label. Matching runs in both directions.
- Sixteen feature orders, paired with their reverses, estimate Shapley
  contributions to DR. Features with attribution at least 0.05 are replaced
  once, then a fresh model is fitted once.
- Numerical standardisation, categorical one-hot encoding and German account
  imputation are fitted on training rows only. Test rows are never modified.
- Female = 0, male = 1. A favourable outcome is good credit, no recorded
  two-year recidivism, or income above $50,000. DIR is the female/male
  favourable-outcome ratio. DP_Diff is the absolute difference between those
  rates. Consistency uses five neighbours, allowing self matches, with sex
  excluded from the distance.

This is a small implementation of the method, rather than an exact
reproduction of the paper's five-fold KernelSHAP experiment. German/COMPAS
outcomes are also coded in the favourable direction, unlike the authors'
loaders. The notebook explains these differences beside the comparison.

## Observed results

| Dataset | Baseline DP | FairSHAP DP | Baseline accuracy | FairSHAP accuracy |
|---|---:|---:|---:|---:|
| German Credit | 0.0519 | 0.0858 | 0.7100 | 0.7150 |
| COMPAS | 0.1752 | 0.1280 | 0.6701 | 0.6632 |
| Adult | 0.1799 | 0.1673 | 0.8693 | 0.8681 |

DR decreased on all three datasets, but group fairness did not improve in
every case. German Credit's DP became worse. One split and a finite
attribution budget do not support claims of statistical significance.

The `results/` folder contains CSV tables, the comparison figure and audit
arrays. `provenance.json` records the settings, software versions, dataset
URLs and file hashes. `requirements.txt` lists the exact packages installed
automatically by the first notebook cell. `run_notebook.py` is an optional
automation helper; it is not needed for the steps above.
