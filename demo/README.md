# Stage I thin-slice demo

`wrong_connector_evidence/` is a fully synthetic evidence pack for incident `INC-WC-001`. It contains a manually annotated frame record, a barcode event, an active BOM, and an active SOP.

Run from the repository root:

```bash
python3 -m src.soplens_thin_slice --evidence-dir demo/wrong_connector_evidence
```

To save the JSON report:

```bash
python3 -m src.soplens_thin_slice \
  --evidence-dir demo/wrong_connector_evidence \
  --output /tmp/soplens_stage1_report.json
```

The evidence is synthetic and team-authored. The frame record is a manual annotation, not computer-vision output. The prototype does not run an LLM, speech model, agent framework, or B70 workload.
