# Reproducibility and provenance

## 1. Primary population

The controlled study uses four MaDI-Bench base-task domains: Products, Companies, Music, and Scientific Papers.

Games is outside the primary analysis because the released fusion artifact does not expose complete source membership for all 100 reference entities. The controlled intervention changes known entity membership. Including unresolved Games membership would make the intervention itself uncertain, so the paper leaves that domain out of the primary controlled study.

Companies uses a cleaned 96-entity population. Four reference anchors are removed because the released labels assign a source record to more than one entity. The retained checkpoint records the excluded anchors and duplicate members.

## 2. Controlled perturbation

For each domain, one movable source is fixed. For an ordered set of `k` eligible reference clusters, one record from that source is cyclically reassigned to the next selected cluster. Every affected cluster loses one record and receives one record from the same source. Cluster size and source composition are therefore preserved.

The paper evaluates `k ∈ {5, 10, 15, 20, 25, 30}`. Within a fixed `(domain, k)` matched comparison, the number of affected clusters, false-positive and false-negative link counts, moved source, cluster-size multiset, source composition, pairwise F1, B³ F1, and CEAF_e F1 are fixed.

## 3. DCI and downstream damage

Downstream Correspondence Impact (DCI) counts fused output cells whose values change when a correspondence perturbation is passed through the domain's fixed fusion policy. DCI uses source values and the fusion policy. It does not use the fusion reference.

Downstream damage is evaluated later against the fusion reference as the loss in fused-table cell accuracy relative to the baseline grouping.

## 4. Evidence layers retained here

### Main controlled comparison

`data/EDBT2027_MaDI_4domain_checkpoint_v2.json` stores the controlled populations, the selected low/high-DCI matched results for all 24 `(domain, k)` strata, and the within-stratum DCI–damage Spearman summaries.

### Simple-proxy falsification

`data/EDBT2027_MaDI_DCI_proxy_ablation_v4.md` is the retained checkpoint from the marginal proxy analysis. It compares DCI with non-null count, destination disagreement, unique-value count, and a fusion-agnostic candidate-set change measure. Products remains a genuine counterexample to universal marginal DCI dominance.

### Independent incremental analysis

`data/EDBT2027_MaDI_DCI_incremental_v5.json` stores cross-product matrices and summary results for an independent 12,000-perturbation resampling run. Predictors and signed damage were rank-transformed and centered within each `(domain, k)` stratum. The four simple proxies are fit jointly, then DCI is added. The same checkpoint contains leave-one-domain-out evaluation.

### Domain-level stability

`data/EDBT2027_MaDI_domain_robustness_v6.json` stores the whole-domain bootstrap and delete-one-domain calculations used to characterize cross-domain stability. With four domains, the paper treats these calculations as robustness evidence and does not present them as high-resolution cluster-level significance tests.

## 5. Upstream inputs

The source tables, mappings, fusion-test references, and domain fusion configurations come from MaDI-Bench. Fusion and scoring behavior follows the PyDI semantics used by that benchmark.

For reconstruction work, use the contemporaneous MaDI-Bench v2 release:

- MaDI-Bench commit: `6b2b43d8116b2dd36fc9a83c249d295941af069e`
- PyDI commit pinned by that release: `cd51e25e5e7f0493c45f678d0d0ef6e123d9133a`

Upstream repositories:

- https://github.com/wbsg-uni-mannheim/MaDI-Bench
- https://github.com/wbsg-uni-mannheim/PyDI

The upstream data are not redistributed here.

## 6. Reproducibility boundary

The retained checkpoints are sufficient to audit the manuscript-level numerical summaries checked by `scripts/verify_reported_results.py`.

They are not a complete archive of every exploratory sample generated during the study. In particular, the exact v4 sample-level perturbation rows and random seeds were not retained. The v5 incremental analysis was run as an independent resampling under the same fixed `(domain, k)` design. The manuscript keeps the v4 marginal results and v5 incremental results separate for that reason.

The artifact therefore supports numerical audit of the reported retained analyses. It does not claim bit-for-bit regeneration of the original exploratory perturbation streams from raw source tables.
