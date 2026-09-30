#!/usr/bin/env python3
"""Extract the tabular benchmark records from OOD-VoiceBench-v1.0-compact.pdf.

The compact PDF contains complete prompt/attribute/transcript fields. In the
provided export, canonical_rewrite is populated for ID Reference rows (where
it duplicates the canonical prompt) but is blank for OOD rows; the extractor
preserves that distinction instead of inventing rewrites.
"""
from __future__ import annotations
import csv, json, re
from pathlib import Path
from pypdf import PdfReader

PDF = Path(__file__).resolve().parents[1] / "source" / "OOD-VoiceBench-v1.0-compact.pdf"
OUT = Path(__file__).resolve().parents[1] / "data"
ID_RE = re.compile(r"^VB\d{4}$")
TRANS_RE = re.compile(r"^t\d+$")
AXES = {"ID Reference", "Style OOD", "Lexical OOD", "Compositional OOD"}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def read_records() -> list[dict]:
    pages = PdfReader(str(PDF)).pages
    text = "\n".join(p.extract_text() or "" for p in pages)
    starts = list(re.finditer(r"(?m)^VB\d{4}$", text))
    rows = []
    for idx, m in enumerate(starts):
        block = text[m.start(): starts[idx + 1].start() if idx + 1 < len(starts) else len(text)]
        raw_lines = [norm(x) for x in block.splitlines() if norm(x)]
        benchmark_id = raw_lines.pop(0)
        # Remove page/table headers that can occur inside a block boundary.
        header_re = re.compile(r"^(OOD-VoiceBench v1\.0|Page \d+|ID Reference \(250\)|Style OOD \(250\)|Lexical OOD \(250\)|Compositional OOD \(250\)|ID|Axis|Sub-axis|Prompt|Canonical rewrite|Attributes|Transcript ID|Focus / notes)$")
        lines = [x for x in raw_lines if not header_re.fullmatch(x)]
        axis = lines.pop(0)
        if axis not in AXES:
            raise ValueError(f"{benchmark_id}: unexpected axis {axis!r}")
        sub_axis = lines.pop(0)
        # PDF line wrapping splits mixed_standard_attributes into two lines.
        if lines and sub_axis == "mixed_standard_attribute" and lines[0] == "s":
            sub_axis += lines.pop(0)
        # Find transcript ID; everything before it is prompt/rewrite/attributes.
        ti = next((i for i, x in enumerate(lines) if TRANS_RE.fullmatch(x)), None)
        if ti is None:
            raise ValueError(f"{benchmark_id}: transcript id not found")
        content, tail = lines[:ti], lines[ti + 1:]
        transcript_id = lines[ti]
        focus_parts = [x.strip().strip("|").strip() for x in tail if x and x != "|"]
        focus_notes = " | ".join(x for x in focus_parts if x)
        if axis == "ID Reference":
            if not content:
                raise ValueError(f"{benchmark_id}: empty ID content")
            attributes = content[-1]
            pre = "".join(content[:-1])
            if len(pre) % 2 == 0 and pre[:len(pre)//2] == pre[len(pre)//2:]:
                prompt = pre[:len(pre)//2]
                canonical_rewrite = prompt
            else:
                # Keep unusual rows inspectable rather than silently dropping text.
                half = len(pre) // 2
                prompt, canonical_rewrite = pre[:half], pre[half:]
        else:
            # In the supplied compact export the OOD rows expose prompt, intended
            # attributes, and transcript_id; canonical_rewrite cells are blank.
            if len(content) < 2:
                raise ValueError(f"{benchmark_id}: insufficient OOD content")
            prompt = "".join(content[:-1])
            attributes = content[-1]
            canonical_rewrite = ""
        rows.append({
            "benchmark_id": benchmark_id,
            "axis": axis,
            "sub_axis": sub_axis,
            "prompt": prompt,
            "canonical_rewrite": canonical_rewrite,
            "attributes": attributes,
            "transcript_id": transcript_id,
            "focus_notes": focus_notes,
        })
    return rows


def main() -> None:
    rows = read_records()
    assert len(rows) == 1000, len(rows)
    assert [r["benchmark_id"] for r in rows] == [f"VB{i:04d}" for i in range(1, 1001)]
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "OOD-VoiceBench-v1.0.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    with (OUT / "OOD-VoiceBench-v1.0.jsonl").open("w", encoding="utf-8") as f:
        for row in rows: f.write(json.dumps(row, ensure_ascii=False) + "\n")
    by_axis = {}
    for row in rows: by_axis[row["axis"]] = by_axis.get(row["axis"], 0) + 1
    print("records", len(rows), "by_axis", by_axis)
    print("ood_rows_with_empty_canonical_rewrite", sum(not r["canonical_rewrite"] for r in rows if r["axis"] != "ID Reference"))

if __name__ == "__main__":
    main()
