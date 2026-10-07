# Paper-to-artifact map

This page points each reported analysis to the retained file that supports it.

| Manuscript result | Artifact source |
| --- | --- |
| Controlled populations and eligible clusters | `data/EDBT2027_MaDI_4domain_checkpoint_v2.json` → `population` |
| Low/high-DCI matched comparisons across 24 `(domain, k)` strata | `data/EDBT2027_MaDI_4domain_checkpoint_v2.json` → `results` |
| 23 wins, one tie, no reversals; mean/median/max matched gaps | `data/EDBT2027_MaDI_4domain_checkpoint_v2.json` → `headline` and `results` |
| Random within-stratum DCI–damage Spearman associations | `data/EDBT2027_MaDI_4domain_checkpoint_v2.json` → `within_k_dci_damage_spearman` |
| Marginal comparison with four simple content proxies | `data/EDBT2027_MaDI_DCI_proxy_ablation_v4.md` |
| Products counterexample to universal marginal DCI dominance | `data/EDBT2027_MaDI_DCI_proxy_ablation_v4.md` |
| 12,000-perturbation joint simple-proxy vs. simple-plus-DCI analysis | `data/EDBT2027_MaDI_DCI_incremental_v5.json` → `results.pooled_rank_FE` |
| Within-domain incremental `R^2` | `data/EDBT2027_MaDI_DCI_incremental_v5.json` → `results.within_domain` |
| Leave-one-domain-out transfer | `data/EDBT2027_MaDI_DCI_incremental_v5.json` → `results.leave_one_domain_out` |
| Exact 256-sample whole-domain bootstrap | `data/EDBT2027_MaDI_domain_robustness_v6.json` → `cluster_bootstrap` |
| Delete-one-domain robustness | `data/EDBT2027_MaDI_domain_robustness_v6.json` → `leave_one_domain_out_training_sensitivity` |

For a compact numerical check, run:

```bash
python scripts/verify_reported_results.py
```
