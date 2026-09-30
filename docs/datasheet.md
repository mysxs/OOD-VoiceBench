# OOD-VoiceBench v1.0 Datasheet

## Motivation

OOD-VoiceBench evaluates whether prompt-based voice-design systems preserve requested voice attributes when users describe voices through non-canonical language.

## Composition

The release contains 1,000 Chinese prompts: 250 ID Reference, 250 Style OOD, 250 Lexical OOD, and 250 Compositional OOD. Each OOD axis is divided into three sub-axes with 83–84 items each.

## Fields

- `benchmark_id`: stable item identifier (`VB0001`–`VB1000`).
- `axis`: one of the four splits.
- `sub_axis`: fine-grained OOD or ID category.
- `prompt`: user-style or canonical voice description.
- `canonical_rewrite`: canonical rewrite when present in the supplied export.
- `attributes`: intended attribute tags visible in the supplied export.
- `transcript_id`: identifier of the paired TTS transcript.
- `focus_notes`: evaluation dimensions included in the supplied export.

## Construction and filtering

The compact PDF describes a two-stage construction process: raw prompt collection followed by deduplication, safety filtering, length checks, and balanced sampling. The PDF does not provide annotator identities or personally identifying information.

## Known limitations of this repository snapshot

The supplied compact PDF does not expose OOD canonical-rewrite strings or the transcript text/audio files. The OOD `canonical_rewrite` cells are therefore empty in the tabular exports. This repository is a faithful machine-readable transcription of the supplied PDF, not a reconstruction of unavailable fields.

The benchmark is Chinese-only and OOD is defined relative to the released canonical reference distribution. The private training distributions of evaluated systems are not assumed to be known.

## Ethical use

Do not use the benchmark to target identifiable private individuals. Review prompts for privacy, safety, cultural context, and downstream misuse before deployment.
