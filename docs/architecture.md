# Proposed architecture

## Input layer

- Short video clips and time-coded frames
- Operator audio
- Synthetic equipment and barcode events
- Team-authored SOP and BOM revisions

## Evidence pipeline

The pipeline normalizes timestamps, records document revision identifiers, preserves source hashes, and links extracted observations to the original evidence.

## Agent roles

1. The perception component extracts parts, actions, text, speech, and timestamps.
2. The retrieval component selects the exact controlled document revision.
3. The hypothesis component ranks candidate causes and identifies the checks needed to distinguish them.
4. The verifier checks citations, rejects unsupported claims, and requests human review when evidence is incomplete or conflicting.

## Output

The system returns a structured report containing the evidence timeline, ranked candidate causes, citations, open questions, and the next human-approved inspection step.

## Safety boundary

SOPLens is not a safety-certified control system. The prototype will not connect to production PLC control paths or issue autonomous stop, repair, or release commands.
