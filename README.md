# OOD-VoiceBench v1.0

OOD-VoiceBench is a benchmark for evaluating prompt-based voice-design systems under realistic user-expression shifts. It contains 1,000 Chinese voice-design prompts divided into a canonical reference split and three OOD axes:

| Split | Count | Description |
|---|---:|---|
| ID Reference | 250 | Canonical caption-style prompts |
| Style OOD | 250 | Colloquial, metaphorical, and scenario-based descriptions |
| Lexical OOD | 250 | Synonyms, slang, dialectal, and non-canonical wording |
| Compositional OOD | 250 | Rare combinations, contradictory constraints, and persona bundles |

## Files

- `data/OOD-VoiceBench-v1.0.csv`: UTF-8 CSV export.
- `data/OOD-VoiceBench-v1.0.jsonl`: UTF-8 JSON Lines export.
- `source/OOD-VoiceBench-v1.0-compact.pdf`: the supplied compact release containing all 1,000 items.
- `docs/datasheet.md`: benchmark scope, construction, and intended use.
- `tools/extract_benchmark.py`: deterministic extraction script used to produce the initial CSV and JSONL files from the supplied PDF.
- `tools/reconstruct_rewrites.py`: deterministic generation of attribute-preserving canonical voice descriptions.

Each row contains `benchmark_id`, `axis`, `sub_axis`, `prompt`, `canonical_rewrite`, `attributes`, `transcript_id`, and `focus_notes`.

## Important release note

The `canonical_rewrite` field gives a concise, caption-style voice description. For OOD rows, each description is generated deterministically from the released attribute tags, preserving every listed attribute and adding no unsupported acoustic property.

The benchmark is currently Chinese-only. It is intended to measure shifts relative to the canonical reference distribution; it does not establish that every item is outside every evaluated system's private training distribution.

## Reproduce the tabular export

The extraction helper requires Python and `pypdf`:

```bash
python tools/extract_benchmark.py
python tools/reconstruct_rewrites.py
```

Run the reconstruction step after extraction if you want the supplementary OOD rewrite values; extraction alone reproduces the blanks in the compact PDF.

## Intended use

The benchmark is intended for research on prompt following, robustness, speech generation, and evaluation. It should not be used to imitate identifiable private individuals. Users should apply their own safety and privacy review before deploying models with these prompts.

## License

No dataset license is asserted in this initial repository snapshot. Please add the license selected by the dataset authors before treating the files as broadly redistributable.

## Citation

```bibtex
@misc{oodvoicebench2026,
  title={OOD-VoiceBench: Benchmarking Prompt-Based Voice Design under Realistic User-Expression Shifts},
  year={2026},
  howpublished={\url{https://github.com/mysxs/OOD-VoiceBench}}
}
```
