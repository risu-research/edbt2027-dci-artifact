#!/usr/bin/env python3
"""Check manuscript-level summaries against the retained EDBT 2027 checkpoints.

The verifier uses only Python's standard library. It recomputes summary values from
retained checkpoints; it does not redownload MaDI-Bench or regenerate the original
perturbation streams.
"""
from pathlib import Path
import json
import statistics

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    with (DATA / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def close(a, b, tol=1e-6):
    return abs(float(a) - float(b)) <= tol


def pick(d, *keys):
    for key in keys:
        if key in d:
            return d[key]
    raise KeyError(keys)


v2 = load("EDBT2027_MaDI_4domain_checkpoint_v2.json")
v5 = load("EDBT2027_MaDI_DCI_incremental_v5.json")
v6 = load("EDBT2027_MaDI_domain_robustness_v6.json")

# 1. Matched low/high-DCI comparison.
gaps = []
wins = ties = reversals = 0
for rows in v2["results"].values():
    for row in rows:
        gap = float(row["gap_pp"])
        gaps.append(gap)
        if gap > 1e-12:
            wins += 1
        elif gap < -1e-12:
            reversals += 1
        else:
            ties += 1

assert len(gaps) == 24
assert (wins, ties, reversals) == (23, 1, 0)
assert close(sum(gaps) / len(gaps), v2["headline"]["gap_pp_mean"], 1e-5)
assert close(statistics.median(gaps), v2["headline"]["gap_pp_median"], 1e-5)
assert close(max(gaps), v2["headline"]["gap_pp_max"], 1e-5)

# 2. Random within-stratum DCI-damage associations.
rhos = []
for vals in v2["within_k_dci_damage_spearman"].values():
    rhos.extend(float(value) for key, value in vals.items() if key != "mean")
assert len(rhos) == 24
assert all(value > 0 for value in rhos)
assert close(sum(rhos) / len(rhos), 0.430756, 1e-6)
assert close(statistics.median(rhos), 0.430874, 1e-6)

# 3. Independent incremental-value analysis.
pooled = v5["results"]["pooled_rank_FE"]
simple = float(pick(pooled, "simple_only_R2", "simple_R2", "R2_simple"))
full = float(pick(pooled, "simple_plus_DCI_R2", "full_R2", "R2_full"))
delta = float(pick(pooled, "delta_R2", "delta_r2"))
partial = float(pick(pooled, "partial_R2_DCI_given_simples", "partial_R2"))
assert close(simple, 0.0850, 5e-4)
assert close(full, 0.2888, 5e-4)
assert close(delta, 0.2037, 5e-4)
assert close(partial, 0.2227, 5e-4)

# 4. Leave-one-domain-out evaluation.
held_out = {}
for domain, row in v5["results"]["leave_one_domain_out"].items():
    if domain == "pooled" or not isinstance(row, dict):
        continue
    held_out[domain] = float(pick(row, "delta_R2", "delta_r2"))
assert set(held_out) == {"products", "companies_clean", "music", "papers"}
assert all(value > 0 for value in held_out.values())
pooled_held_out = v5["results"]["leave_one_domain_out"]["pooled"]
assert close(pooled_held_out["simple_R2"], 0.0428, 5e-4)
assert close(pooled_held_out["full_R2"], 0.1919, 5e-4)
assert close(pooled_held_out["delta_R2"], 0.1491, 5e-4)

# 5. Whole-domain robustness.
boot = v6["cluster_bootstrap"]
assert int(boot["n_exact_resamples"]) == 256
boot_delta = boot["delta_R2"]
assert int(pick(boot_delta, "positive_resamples", "positive_count", "n_positive")) == 256
ci_low, ci_high = boot_delta["percentile_95_CI"]
assert close(ci_low, 0.1089, 5e-4)
assert close(ci_high, 0.3910, 5e-4)

leave_one_out = v6["leave_one_domain_out_training_sensitivity"]
assert set(leave_one_out) == {"products", "companies_clean", "music", "papers"}
assert all(float(row["delta_R2"]) > 0 for row in leave_one_out.values())

print("PASS — retained checkpoints are internally consistent with the manuscript summaries")
print(f"Matched strata: {len(gaps)} | wins/ties/reversals = {wins}/{ties}/{reversals}")
print(
    "Matched gap mean/median/max (pp): "
    f"{sum(gaps)/len(gaps):.4f} / {statistics.median(gaps):.4f} / {max(gaps):.4f}"
)
print(f"Random DCI-damage Spearman strata positive: {sum(x > 0 for x in rhos)}/{len(rhos)}")
print(f"Mean/median within-stratum rho: {sum(rhos)/len(rhos):.4f} / {statistics.median(rhos):.4f}")
print(f"Incremental R^2: {simple:.4f} -> {full:.4f} (delta {delta:+.4f}; partial {partial:.4f})")
print("Held-out domain delta R^2:")
for domain in ("products", "companies_clean", "music", "papers"):
    print(f"  {domain}: {held_out[domain]:+.4f}")
print(f"Pooled held-out delta R^2: {float(pooled_held_out['delta_R2']):+.4f}")
print(f"Whole-domain bootstrap positive resamples: {int(boot_delta['positive_resamples'])}/256")
print(f"Whole-domain bootstrap 95% interval: [{float(ci_low):.4f}, {float(ci_high):.4f}]")
print("Delete-one-domain delta R^2:")
for domain in ("products", "companies_clean", "music", "papers"):
    print(f"  remove {domain}: {float(leave_one_out[domain]['delta_R2']):+.4f}")
