"""Prepare canonical voice descriptions for the benchmark.

The descriptions explicitly list the attributes associated with each item and
avoid adding unsupported speaker identity or acoustic properties.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "OOD-VoiceBench-v1.0.csv"
JSONL_PATH = ROOT / "data" / "OOD-VoiceBench-v1.0.jsonl"


def make_rewrite(row: dict[str, str]) -> str:
    attrs = [part.strip() for part in row["attributes"].split(",") if part.strip()]
    if not attrs:
        raise ValueError(f"{row['benchmark_id']} has no attributes")
    joined = "、".join(attrs)
    axis = row["axis"]
    if axis == "Style OOD":
        if row["sub_axis"] == "metaphorical":
            prefix = "声音的音色质感呈现"
        elif row["sub_axis"] == "scenario":
            prefix = "声音整体呈现出相应场景中的说话风格，具体表现为"
        else:
            prefix = "声音整体呈现以下表达特点"
    elif axis == "Lexical OOD":
        prefix = "声音的音色、语气和表达特征为"
    elif axis == "Compositional OOD":
        prefix = "声音同时具备以下组合属性"
    else:
        raise ValueError(f"unexpected axis: {axis}")
    return f"{prefix}：{joined}。"


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    changed = 0
    for row in rows:
        if row["axis"] != "ID Reference":
            row["canonical_rewrite"] = make_rewrite(row)
            changed += 1

    if changed != 750:
        raise RuntimeError(f"expected 750 missing OOD rewrites, filled {changed}")

    fields = list(rows[0])
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    with JSONL_PATH.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"prepared {changed} OOD canonical_rewrite values")


if __name__ == "__main__":
    main()
