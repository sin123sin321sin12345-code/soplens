# SOPLens

SOPLens is ProofLine Lab's Stage I proposal for the ASUS UGen AI League 2026, Battlefield Thunderstorm track, under Workplace AI.

## Project status

This repository documents a Stage I system design and includes a minimal deterministic evidence-linking prototype. It does not contain model inference or measured B70 results. All performance thresholds in the proposal are planned Stage II validation targets.

## Stage I executable thin slice

The Stage I prototype reads a synthetic wrong-connector evidence pack containing a frame observation, barcode event, active BOM, and active SOP. It produces a JSON incident report whose material claims cite source IDs. The verifier rejects an intentionally unsupported stale-work-instruction hypothesis because neither cited controlled document supports a stale status.

Run the prototype from the repository root:

```bash
python3 -m src.soplens_thin_slice --evidence-dir demo/wrong_connector_evidence
```

Requirements: Python 3.10 or later. The thin slice uses only the Python standard library.

Run the standard-library unit tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

This thin slice validates deterministic evidence loading, source hashing, source-ID traceability, and explicit verification rules only. It does not perform computer vision, speech recognition, LLM reasoning, semantic entailment, or B70 benchmarking. Those remain Stage II work in the organizer-provided environment.

## Problem

An anomaly alert does not explain why an electronics assembly incident occurred. A line leader or quality engineer still has to align video, operator audio, equipment events, the active BOM, and the correct SOP revision before discussing a cause.

## Proposed system

SOPLens creates a time-aligned evidence graph from controlled inputs. Separate components handle perception, document retrieval, candidate-cause generation, and verification. The verifier rejects material claims that lack a valid citation. The output is a cited incident report for human review.

The first prototype scope is one tabletop wrong-part incident. It supports investigation only. It cannot stop equipment, approve repairs, or release a production lot.

## Hardware baseline

Stage II is designed around one ASUS UGen Intel Arc Pro B70 32GB. Candidate runtimes include OpenVINO, PyTorch XPU, and vLLM XPU. Exact model versions, quantization settings, and residency plans will be selected after profiling the organizer-provided environment.

## Repository plan

- `docs/`: architecture and attribution notes
- `configs/`: candidate model and runtime declarations
- `tests/scenarios/`: controlled validation scenario definitions
- `src/`: the Stage I deterministic thin slice; Stage II model integration is not included

## Data and licensing

The initial validation set will use team-owned tabletop recordings, synthetic equipment logs, team-authored SOP and BOM documents, and signed participant releases. Dependencies must pass a license review before use.

## Team

- Team: ProofLine Lab
- Team lead: 黃捷思
- Team member: 陳信
