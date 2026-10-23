"""Check the published table and derived metrics with the Python standard library."""

import csv
from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rows(filename):
    with (ROOT / "results" / filename).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate():
    rows = read_rows("model_comparison.csv")
    assert [int(row["branches"]) for row in rows] == [2, 3, 4]

    reductions = []
    for row in rows:
        ap_before = float(row["ap_baseline"])
        ap_after = float(row["ap_early_exit"])
        cost_before = float(row["gmac_baseline"])
        cost_after = float(row["gmac_early_exit"])
        assert 0 < ap_after <= ap_before < 1
        assert 0 < cost_after < cost_before
        assert 0 < float(row["early_exit_pct"]) < 100
        assert int(row["layer"]) == 61

        reduction = 100 * (1 - cost_after / cost_before)
        retained = 100 * ap_after / ap_before
        reductions.append(reduction)
        print(f'{row["branches"]}B: {reduction:.2f}% menos GMAC; {retained:.2f}% do AP preservado (AP arredondado)')

    assert isclose(reductions[0], 3.04, abs_tol=0.02)
    assert isclose(reductions[1], 4.48, abs_tol=0.02)
    assert isclose(reductions[2], 4.21, abs_tol=0.02)

    layers = read_rows("layer_search.csv")
    assert [int(row["layer"]) for row in layers] == [49, 52, 55, 58, 61]
    assert all(float(row["gmac"]) > 0 for row in layers)

    thresholds = read_rows("threshold_calibration.csv")
    assert len(thresholds) == 6
    assert all(float(a["early_exit_pct"]) > float(b["early_exit_pct"])
               for a, b in zip(thresholds, thresholds[1:]))
    assert len(read_rows("gate_calibration.csv")) == 4
    print("Tabelas consistentes com os valores conferidos da apresentação.")


if __name__ == "__main__":
    validate()
