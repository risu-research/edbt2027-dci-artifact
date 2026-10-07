# EDBT 2027 MaDI-Bench — DCI vs Simple-Proxy Falsification Ablation (v4)

Date: 2026-10-07

## Question
Does operator-aware Downstream Correspondence Impact (DCI) predict downstream fusion damage better than simpler gold-free content proxies under the same source-preserving cyclic perturbations?

## Design
Primary domains remain Products, Companies-clean, Music, and Papers. Games remains excluded from the gold-controlled primary analysis because its fusion gold does not expose complete source membership.

For each domain and k in {5,10,15,20,25,30}, 500 seeded source-preserving cyclic permutations were generated. Within each fixed (domain,k) stratum, structural matching metrics are constant by construction. Each perturbation was scored against signed downstream damage and five gold-free predictors:

1. `nonnull_count`: non-empty target attributes carried by moved records.
2. `source_disagreement`: moved value disagrees with at least one destination-cluster value.
3. `unique_value_count`: moved record uniquely supplies an origin-cluster value.
4. `fuser_agnostic_diff`: candidate-value multiset changes, without invoking the fusion operator.
5. `DCI`: actual fused output cells changed under the fixed fusion operator.

Primary statistic: within-stratum Spearman rho with signed downstream damage.

## Replay validation
The ablation used current public MaDI-Bench normalized source outputs and the pinned PyDI resolver semantics.

- Products: 100 entities, 72 eligible four-source clusters. Current-source replay baseline 708/836. The main v2 paper checkpoint intentionally freezes the earlier qualification absolute baseline at 693/836, so ablation damage ranks are kept separate from the main absolute-accuracy table.
- Companies-clean: exact membership reconstruction recovered 96 clean entities, 244 unique records, 148 true edges, 52 eligible three-source clusters, and the two known duplicate members (`DBpedia Petronas`, `fullcontact_513`). Current-source replay baseline 387/584 vs the frozen qualification baseline 393/584.
- Music: membership exactly reproduced 1 singleton, 80 MB+Discogs, 12 MB+Last.fm, 7 three-source entities; 80 eligible MB+Discogs clusters. Replay baseline 524/726 vs frozen checkpoint 527/726.
- Papers: all 300 gold source rows recovered; 100 three-source entities; replay baseline exactly 842/922, matching the frozen checkpoint.

Because the ablation tests within-replay rank association, the small Products/Companies/Music absolute-baseline shifts do not change the proxy-vs-DCI comparison. Do not substitute these replay baselines into the main v2 accuracy table.

## Domain-mean within-k Spearman rho

| Domain | nonnull | disagreement | unique | fuser-agnostic | DCI | Best simple | DCI - best simple |
|---|---:|---:|---:|---:|---:|---:|---:|
| Products | 0.382 | 0.361 | 0.412 | 0.173 | 0.288 | 0.414 | -0.126 |
| Companies-clean | 0.045 | 0.079 | -0.165 | 0.047 | 0.193 | 0.081 | +0.111 |
| Music | constant | 0.105 | -0.137 | 0.243 | 0.522 | 0.243 | +0.279 |
| Papers | 0.107 | 0.227 | -0.109 | 0.286 | 0.731 | 0.288 | +0.443 |

## Aggregate across 24 fixed-(domain,k) strata

| Metric | Mean rho | Median rho |
|---|---:|---:|
| DCI | **0.433** | **0.408** |
| source_disagreement | 0.193 | 0.174 |
| fuser_agnostic_diff | 0.187 | 0.212 |
| nonnull_count | 0.178 over 18 non-constant strata | 0.102 |
| unique_value_count | 0.000 | -0.119 |

### Strongest direct operator-awareness comparison
DCI beat `fuser_agnostic_diff` in **24/24 strata**.

- Mean paired rho advantage: **+0.246**.
- Median paired advantage: **+0.223**.
- Minimum advantage: **+0.0369**.
- Maximum advantage: **+0.4929**.
- One-sided exact sign test: **p = 5.96e-8**.
- One-sided paired Wilcoxon: **p = 5.96e-8**.
- Bootstrap 95% CI for mean advantage: **[0.193, 0.302]**.

This is the cleanest evidence that invoking the actual downstream fusion operator adds predictive information beyond merely observing that candidate values changed.

### Adversarial “best simple proxy” comparison
For each stratum, choose the strongest of the four simple proxies *after seeing the outcome* (an intentionally favorable oracle for the baselines).

- DCI wins: **18/24 strata**.
- DCI loses: **6/24 strata**.
- All 6 losses are Products.
- Mean DCI-minus-oracle-simple rho: **+0.177**.
- Median: **+0.191**.
- One-sided sign test: **p = 0.0113**.
- One-sided paired Wilcoxon: **p = 0.000700**.
- Bootstrap 95% CI for mean advantage: **[0.091, 0.261]**.

## Important falsification result
The strong universal claim is false:

> DCI is not always the best content-aware predictor.

Products is a real counterexample. There, simple record richness / unique-value proxies outperform DCI in all six k strata. This should be retained, not patched away.

The supported claim is narrower and stronger scientifically:

> Across four domains, operator-aware DCI is substantially more predictive of downstream fusion damage on average than simple gold-free content proxies, and it dominates a fuser-agnostic candidate-change proxy in every tested fixed-topology stratum. The advantage is heterogeneous: Products favors simpler richness proxies, while Companies, Music, and Papers favor DCI.

## Paper framing after falsification
Do **not** claim universal dominance or present DCI as the only valid downstream-risk measure.

Recommended framing:
- Conventional EM metrics are structurally blind to unequal downstream cost.
- Gold-free content-aware measures recover some of that missing information.
- Operator-aware DCI is the strongest overall predictor in this experiment and adds a clear advantage over fuser-agnostic change counts.
- Domain heterogeneity matters; Products demonstrates that simple record richness can sometimes be more informative.

This result is more defensible than a universal-superiority claim because the ablation was designed to falsify DCI and did uncover a genuine failure mode.

## Remaining secondary robustness
The next optional analysis is a multivariate incremental-value test: within-stratum rank regression using the four simple proxies jointly, then adding DCI, with leave-one-domain-out validation. This is useful for quantifying incremental value beyond a *combination* of simple proxies, but the primary individual-proxy falsification question is already answered.