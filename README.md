# EDBT 2027 artifact: Unequal Downstream Consequences of Entity-Matching Errors in Data Fusion

This repository accompanies the EDBT 2027 Experiments & Analysis submission **“Unequal Downstream Consequences of Entity-Matching Errors in Data Fusion.”** It provides the retained checkpoints behind the reported numerical results and a small verifier that recomputes the manuscript-level summaries from those checkpoints.

The artifact is intentionally narrow. It includes the material needed to audit the reported results without redistributing MaDI-Bench, and it keeps the original analysis stages separate instead of collapsing them into one post hoc file.

## Contents

- `data/EDBT2027_MaDI_4domain_checkpoint_v2.json`  
  Controlled four-domain experiment: populations, matched low/high-DCI comparisons, structural metrics, and within-stratum DCI–damage associations.
- `data/EDBT2027_MaDI_DCI_proxy_ablation_v4.md`  
  Retained falsification checkpoint comparing DCI with four simpler content-aware proxies. It includes the Products counterexample reported in the paper.
- `data/EDBT2027_MaDI_DCI_incremental_v5.json`  
  Independent 12,000-perturbation analysis used for the joint simple-proxy versus simple-plus-DCI comparison and leave-one-domain-out evaluation.
- `data/EDBT2027_MaDI_domain_robustness_v6.json`  
  Whole-domain bootstrap and delete-one-domain robustness calculations used in the cross-domain stability analysis.
- `scripts/verify_reported_results.py`  
  Standard-library Python script that checks the headline quantities reported in the manuscript against the retained checkpoints.
- `docs/REPRODUCIBILITY.md`  
  Experimental scope, upstream dependencies, population decisions, and the exact reproducibility boundary of this artifact.
- `docs/PAPER_MAP.md`  
  Direct map from each manuscript result to the retained checkpoint that supports it.

## Quick verification

Python 3.10 or later is sufficient. The verifier has no third-party dependency.

```bash
python scripts/verify_reported_results.py
```

A successful run ends with:

```text
PASS — retained checkpoints are internally consistent with the manuscript summaries
```

The script checks, among other quantities:

- 24 matched `(domain, k)` strata with 23 high-DCI wins, one tie, and no reversals;
- the reported mean, median, and maximum matched accuracy gaps;
- positive within-stratum DCI–damage association in all 24 strata;
- the pooled `R^2` change from the four simple proxies to the model that adds DCI;
- positive held-out `ΔR^2` for Products, Companies, Music, and Papers;
- positive whole-domain bootstrap increments in all 256 ordered resamples;
- positive delete-one-domain increments after removing each domain in turn.

## Upstream benchmark

The experiment uses the public MaDI-Bench base tasks and PyDI fusion/evaluation semantics from the Data and Web Science Group at the University of Mannheim.

- MaDI-Bench: https://github.com/wbsg-uni-mannheim/MaDI-Bench
- PyDI: https://github.com/wbsg-uni-mannheim/PyDI
- MaDI-Bench paper: https://arxiv.org/abs/2606.30371

The benchmark data are not copied into this repository. For reconstruction work, the contemporaneous MaDI-Bench v2 release is commit `6b2b43d8116b2dd36fc9a83c249d295941af069e`. That release pins PyDI to commit `cd51e25e5e7f0493c45f678d0d0ef6e123d9133a`.

## Scope of reproducibility

This repository supports **numerical audit of the reported analyses from retained checkpoints**. It does not claim a bit-for-bit regeneration of every exploratory perturbation stream from raw source tables.

The main controlled checkpoint preserves the selected matched results and the within-stratum association summaries. The original v4 sample-level rows and exact random seeds were not retained. The v5 analysis is therefore an independent resampling under the same fixed `(domain, k)` design, and the paper reports the v4 marginal analysis and v5 incremental analysis separately. `docs/REPRODUCIBILITY.md` gives the full boundary.

## License

The verification script and documentation in this repository are released under the MIT License. MaDI-Bench and PyDI remain subject to their upstream licenses.
