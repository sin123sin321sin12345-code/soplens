# SOPLens final demo script

Final running time: 2:48. Language: English. The video combines proposal slides with a screen rendered from the executable Stage I thin slice. The screen uses controlled synthetic evidence and is not a B70 benchmark.

## 0:00–0:05 — Introduction

**Visual:** Title slide.

**Narration:**

> We're ProofLine Lab. Our proposal for the Workplace AI track is SOPLens.

## 0:05–0:14 — Investigation gap

**Visual:** The gap after an anomaly alert.

**Narration:**

> A camera can spot a wrong or missing component, but the alert is only the beginning. The line leader still has to reconstruct the event and justify the next inspection step.

## 0:14–0:29 — Current workflow

**Visual:** Disconnected evidence and the current manual workflow.

**Narration:**

> Today, video, equipment logs, work instructions, the bill of materials, and operator notes often sit in separate places. The investigator must align them by time and confirm the active document revision before evaluating possible causes.

## 0:29–0:51 — Executable Stage I thin slice

**Visual:** Actual deterministic output showing four source records and hashes, five accepted claims, one unsupported alternative, six passing tests, and `human_review_required`.

**Narration:**

> This is a controlled Stage I case. The evidence is synthetic. The repository thin slice loads four source records and hashes them. It accepts five cited claims and rejects a stale-instruction alternative. The output remains `human_review_required`.

## 0:51–1:06 — Proposed workflow

**Visual:** Four investigation steps.

**Narration:**

> SOPLens collects those records, aligns timestamps and document versions, evaluates candidate causes, and produces a report for human review. Every material claim must point to a frame, log line, transcript segment, or controlled document.

## 1:06–1:26 — Single-card architecture

**Visual:** Proposed B70 deployment architecture.

**Narration:**

> The proposed Stage II architecture runs locally on one ASUS UGen Intel Arc Pro B70. Video, audio, equipment records, and documents pass through perception and extraction. The application stores timestamps, source hashes, and citations in an evidence graph before it evaluates possible causes.

## 1:26–1:43 — Separated checks

**Visual:** Perception, retrieval, hypothesis, and verification roles.

**Narration:**

> The roles are separated deliberately. The perception agent extracts observations. The retrieval agent finds the exact controlled documents. The hypothesis agent proposes candidate causes. A separate verification agent rejects unsupported statements and requests human review when evidence is missing or conflicting.

## 1:43–1:52 — Human boundary

**Visual:** Operational limits and safeguards.

**Narration:**

> SOPLens supports investigation only. It cannot stop equipment, approve a repair, or release a production lot. A person approves every action.

## 1:52–2:07 — Why the B70

**Visual:** Official B70 specifications mapped to Stage II tests.

**Narration:**

> The B70 is relevant because the workload combines visual analysis, speech recognition, retrieval, and reasoning while incident evidence remains on site. Stage II profiling will determine model quantization, context length, residency, and loading order.

## 2:07–2:13 — Baseline

**Visual:** Single-card Stage II baseline.

**Narration:**

> The required prototype is designed for one B70. Multi-card scaling is optional and will not be used to satisfy the baseline.

## 2:13–2:33 — Validation targets

**Visual:** Stage II validation table. All figures are labeled as targets, not results.

**Narration:**

> Stage II targets include candidate-cause Top-3 at eighty percent or better, correct abstention at ninety percent or better, and citation precision at ninety-five percent or better. Unsupported claims must stay at two percent or less, with p95 latency within thirty seconds. These are acceptance targets, not Stage I results.

## 2:33–2:48 — Exit criteria

**Visual:** Stage II exit criteria.

**Narration:**

> Stage II must prove traceability, correct abstention, and single-card execution. The repository already includes the deterministic thin slice and six tests. Another reviewer must be able to reproduce the result. Thank you.

## Suggested YouTube description

SOPLens is ProofLine Lab's Stage I proposal for ASUS UGen AI League 2026, Battlefield Thunderstorm / Workplace AI. The video includes an executable deterministic thin slice using controlled synthetic evidence. It does not show computer-vision, speech-model, LLM, or B70 performance results. All performance thresholds shown are proposed Stage II acceptance targets. The narration is synthetic and uses the Chatterbox built-in reference voice; no real person's voice was cloned.
