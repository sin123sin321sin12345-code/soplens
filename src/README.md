# Source code

`soplens_thin_slice.py` is a minimal Stage I executable prototype. It loads four synthetic evidence records, builds deterministic material claims, verifies citation presence and source-ID validity, applies one explicit document-status rule, and emits a JSON report.

The verifier deliberately rejects a stale-work-instruction alternative because neither cited controlled document supports a stale status. This demonstrates the intended control path without claiming that the active documents prove which instruction the operator actually saw.

## Stage boundary

Stage I includes:

- JSON evidence loading and schema checks
- source hashes and source-ID traceability
- deterministic wrong-part comparison
- citation-presence and source-ID verification
- an explicit controlled-document status check

Stage I does not include:

- computer vision or speech recognition
- LLM or agent inference
- general semantic entailment checking
- B70 runtime integration or performance measurements

If the proposal advances, Stage II will replace manual synthetic observations with pinned inference components, validate semantic support, and profile the organizer-provided B70 environment.
