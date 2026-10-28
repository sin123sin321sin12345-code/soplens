"""Deterministic Stage I evidence-linking prototype for SOPLens.

This module intentionally uses only the Python standard library. It does not run
AI models and it does not claim ASUS UGen Intel Arc Pro B70 performance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable


REQUIRED_EVIDENCE_FILES = {
    "frame": "frame.json",
    "event": "event.json",
    "bom": "bom.json",
    "sop": "sop.json",
}


class EvidenceError(ValueError):
    """Raised when an evidence pack is missing or internally inconsistent."""


def _read_json(path: Path) -> tuple[dict[str, Any], str]:
    try:
        raw = path.read_bytes()
    except FileNotFoundError as exc:
        raise EvidenceError(f"Missing required evidence file: {path}") from exc

    try:
        record = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"Invalid UTF-8 JSON evidence file: {path}") from exc

    if not isinstance(record, dict):
        raise EvidenceError(f"Evidence record must be a JSON object: {path}")

    return record, hashlib.sha256(raw).hexdigest()


def _require_fields(record: dict[str, Any], fields: Iterable[str], label: str) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise EvidenceError(f"{label} is missing required fields: {', '.join(missing)}")


def load_evidence_pack(
    evidence_dir: Path,
) -> tuple[
    dict[str, dict[str, Any]],
    list[dict[str, str]],
    dict[str, dict[str, Any]],
]:
    """Load and validate the four records in a Stage I evidence pack."""

    records: dict[str, dict[str, Any]] = {}
    source_catalog: list[dict[str, str]] = []
    source_registry: dict[str, dict[str, Any]] = {}
    incident_ids: set[str] = set()

    for expected_type, file_name in REQUIRED_EVIDENCE_FILES.items():
        path = evidence_dir / file_name
        record, sha256 = _read_json(path)
        _require_fields(record, ("source_id", "source_type", "incident_id"), file_name)

        if record["source_type"] != expected_type:
            raise EvidenceError(
                f"{file_name} has source_type={record['source_type']!r}; "
                f"expected {expected_type!r}"
            )

        source_id = str(record["source_id"])
        if source_id in source_registry:
            raise EvidenceError(f"Duplicate source_id: {source_id}")

        incident_ids.add(str(record["incident_id"]))
        records[expected_type] = record
        source_registry[source_id] = {"record": record, "sha256": sha256}

        catalog_entry = {
            "source_id": source_id,
            "source_type": expected_type,
            "file": file_name,
            "sha256": sha256,
        }
        if "revision" in record:
            catalog_entry["revision"] = str(record["revision"])
        if "status" in record:
            catalog_entry["status"] = str(record["status"])
        source_catalog.append(catalog_entry)

    if len(incident_ids) != 1:
        raise EvidenceError(
            "All evidence records must share one incident_id; found "
            + ", ".join(sorted(incident_ids))
        )

    return records, source_catalog, source_registry


def _material_claim(
    claim_id: str,
    category: str,
    text: str,
    citations: list[str],
    support_rule: dict[str, Any] | None = None,
) -> dict[str, Any]:
    claim: dict[str, Any] = {
        "claim_id": claim_id,
        "category": category,
        "material": True,
        "text": text,
        "citations": citations,
        "status": "proposed",
    }
    if support_rule is not None:
        claim["support_rule"] = support_rule
    return claim


def build_proposed_claims(records: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Build deterministic claims from explicit fields in the evidence pack."""

    frame = records["frame"]
    event = records["event"]
    bom = records["bom"]
    sop = records["sop"]

    _require_fields(
        frame,
        ("timestamp", "observed_part_number", "assembly_step"),
        "frame record",
    )
    _require_fields(
        event,
        ("timestamp", "event_type", "part_number", "tray_id"),
        "event record",
    )
    _require_fields(
        bom,
        ("revision", "status", "required_part_number", "assembly_step"),
        "BOM record",
    )
    _require_fields(
        sop,
        ("revision", "status", "instruction", "mismatch_action"),
        "SOP record",
    )

    if bom["status"] != "active" or sop["status"] != "active":
        raise EvidenceError("The Stage I pack requires one active BOM and one active SOP")

    observed_part = str(frame["observed_part_number"])
    event_part = str(event["part_number"])
    required_part = str(bom["required_part_number"])

    if observed_part == required_part:
        raise EvidenceError("The wrong-connector demo requires observed and required parts to differ")
    if event_part != observed_part:
        raise EvidenceError("The barcode event must identify the part recorded in the frame")
    if frame["assembly_step"] != bom["assembly_step"]:
        raise EvidenceError("The frame and BOM must refer to the same assembly step")

    comparison_text = (
        f"The frame record identifies part {observed_part}, while active BOM "
        f"{bom['source_id']} requires {required_part}."
    )

    return [
        _material_claim(
            "CLM-PART-COMPARISON",
            "finding",
            comparison_text,
            [str(frame["source_id"]), str(bom["source_id"])],
        ),
        _material_claim(
            "CLM-EVENT-CORROBORATION",
            "finding",
            (
                f"Event {event['source_id']} records part {event_part} in tray "
                f"{event['tray_id']} during the incident window, matching frame "
                f"{frame['source_id']}."
            ),
            [str(event["source_id"]), str(frame["source_id"])],
        ),
        _material_claim(
            "CLM-SOP-REQUIREMENT",
            "control_requirement",
            (
                f"Active SOP {sop['source_id']} requires the connector part number "
                f"to be checked against active BOM {bom['source_id']} before seating."
            ),
            [str(sop["source_id"]), str(bom["source_id"])],
        ),
        _material_claim(
            "CLM-WRONG-PART-CAUSE",
            "candidate_cause",
            (
                f"A wrong-part connector was present at the {frame['assembly_step']} "
                f"step: observed {observed_part}; required {required_part}."
            ),
            [
                str(frame["source_id"]),
                str(event["source_id"]),
                str(bom["source_id"]),
                str(sop["source_id"]),
            ],
        ),
        _material_claim(
            "CLM-STALE-WORK-INSTRUCTION",
            "alternative_cause",
            "The wrong connector resulted from a stale work instruction.",
            [str(bom["source_id"]), str(sop["source_id"])],
            support_rule={
                "type": "any_source_field_equals",
                "source_ids": [str(bom["source_id"]), str(sop["source_id"])],
                "field": "status",
                "value": "stale",
                "failure_reason": "not_supported_by_cited_sources",
            },
        ),
        _material_claim(
            "CLM-NEXT-INSPECTION",
            "next_inspection",
            (
                f"A human reviewer should hold the assembly step, inspect tray "
                f"{event['tray_id']}, and verify the connector part number against "
                f"active BOM {bom['source_id']} before resuming."
            ),
            [str(event["source_id"]), str(bom["source_id"]), str(sop["source_id"])],
        ),
    ]


def _evaluate_support_rule(
    rule: dict[str, Any],
    source_registry: dict[str, dict[str, Any]],
) -> str | None:
    if rule.get("type") != "any_source_field_equals":
        return "unsupported_verification_rule"

    source_ids = [str(source_id) for source_id in rule.get("source_ids", [])]
    field = str(rule.get("field", ""))
    expected = rule.get("value")

    for source_id in source_ids:
        source = source_registry.get(source_id)
        if source is not None and source["record"].get(field) == expected:
            return None

    return str(rule.get("failure_reason", "support_rule_not_satisfied"))


def verify_claims(
    proposed_claims: list[dict[str, Any]],
    source_registry: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Verify citation presence, source IDs, and explicit deterministic rules.

    This Stage I verifier does not perform general semantic entailment. Claim text
    is generated from deterministic templates over explicit evidence fields.
    """

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    valid_source_ids = set(source_registry)

    for original in proposed_claims:
        claim = deepcopy(original)
        reasons: list[str] = []
        citations = [str(citation) for citation in claim.get("citations", [])]

        if claim.get("material", False) and not citations:
            reasons.append("missing_citation")

        unknown = sorted(set(citations) - valid_source_ids)
        if unknown:
            reasons.append("unknown_source_id:" + ",".join(unknown))

        support_rule = claim.get("support_rule")
        if support_rule is not None and not unknown:
            rule_failure = _evaluate_support_rule(support_rule, source_registry)
            if rule_failure is not None:
                reasons.append(rule_failure)

        if reasons:
            claim["status"] = "rejected"
            claim["verifier_reasons"] = reasons
            rejected.append(claim)
        else:
            claim["status"] = "accepted"
            claim["verifier_reasons"] = []
            accepted.append(claim)

    return accepted, rejected


def build_report(evidence_dir: Path) -> dict[str, Any]:
    """Run the Stage I thin slice and return a deterministic JSON-ready report."""

    records, source_catalog, source_registry = load_evidence_pack(evidence_dir)
    proposed_claims = build_proposed_claims(records)
    accepted, rejected = verify_claims(proposed_claims, source_registry)
    incident_id = str(next(iter(records.values()))["incident_id"])

    return {
        "schema_version": "soplens.stage1.report.v1",
        "incident_id": incident_id,
        "prototype_stage": "Stage I deterministic evidence-linking thin slice",
        "source_catalog": source_catalog,
        "accepted_claims": accepted,
        "rejected_claims": rejected,
        "review_status": "human_review_required",
        "verifier_scope": (
            "Citation presence, source-ID validity, and explicit deterministic rules "
            "only; general semantic entailment is not implemented in Stage I."
        ),
        "stage_boundary": {
            "stage_i_validates": [
                "evidence loading",
                "source hashing and source-ID traceability",
                "deterministic wrong-part comparison",
                "citation-presence control",
                "rejection of a stale-document claim not supported by cited sources",
            ],
            "not_claimed": [
                "computer vision inference",
                "speech recognition",
                "LLM or agent reasoning",
                "general semantic citation verification",
                "ASUS UGen Intel Arc Pro B70 performance",
            ],
        },
    }


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the SOPLens Stage I deterministic evidence-linking prototype."
    )
    parser.add_argument(
        "--evidence-dir",
        type=Path,
        required=True,
        help="Directory containing frame.json, event.json, bom.json, and sop.json.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output path. If omitted, the report is printed to stdout.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        report = build_report(args.evidence_dir)
    except EvidenceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
