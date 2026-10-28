import json
import tempfile
import unittest
from pathlib import Path

from src.soplens_thin_slice import EvidenceError, build_report, verify_claims


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEMO_EVIDENCE = REPOSITORY_ROOT / "demo" / "wrong_connector_evidence"


class StageIThinSliceTests(unittest.TestCase):
    def test_demo_report_accepts_cited_claims_and_rejects_unsupported_stale_document_alternative(self) -> None:
        report = build_report(DEMO_EVIDENCE)

        self.assertEqual(report["incident_id"], "INC-WC-001")
        self.assertEqual(report["review_status"], "human_review_required")

        source_ids = {source["source_id"] for source in report["source_catalog"]}
        self.assertEqual(
            source_ids,
            {"F0142", "E0008", "BOM-RC-L42", "SOP-R62-S8"},
        )

        accepted = {claim["claim_id"]: claim for claim in report["accepted_claims"]}
        rejected = {claim["claim_id"]: claim for claim in report["rejected_claims"]}

        self.assertIn("CLM-WRONG-PART-CAUSE", accepted)
        self.assertIn("CLM-STALE-WORK-INSTRUCTION", rejected)
        self.assertEqual(
            rejected["CLM-STALE-WORK-INSTRUCTION"]["verifier_reasons"],
            ["not_supported_by_cited_sources"],
        )
        self.assertEqual(
            rejected["CLM-STALE-WORK-INSTRUCTION"]["citations"],
            ["BOM-RC-L42", "SOP-R62-S8"],
        )

        next_inspection = accepted["CLM-NEXT-INSPECTION"]["text"]
        self.assertNotIn("quarantine", next_inspection.lower())
        self.assertIn("inspect tray B4", next_inspection)

        for claim in report["accepted_claims"]:
            self.assertTrue(claim["citations"], claim["claim_id"])
            self.assertTrue(set(claim["citations"]).issubset(source_ids), claim["claim_id"])

    def test_verifier_rejects_material_claim_without_citation(self) -> None:
        claims = [
            {
                "claim_id": "CLM-NO-CITATION",
                "category": "alternative_cause",
                "material": True,
                "text": "An unsupported material claim.",
                "citations": [],
                "status": "proposed",
            }
        ]

        accepted, rejected = verify_claims(claims, {})

        self.assertEqual(accepted, [])
        self.assertEqual(rejected[0]["verifier_reasons"], ["missing_citation"])

    def test_verifier_rejects_unknown_source_id(self) -> None:
        claims = [
            {
                "claim_id": "CLM-UNKNOWN",
                "category": "finding",
                "material": True,
                "text": "A material claim with an invalid citation.",
                "citations": ["NOT-A-SOURCE"],
                "status": "proposed",
            }
        ]

        source_registry = {
            "F0142": {"record": {"source_id": "F0142"}, "sha256": "test-hash"}
        }
        accepted, rejected = verify_claims(claims, source_registry)

        self.assertEqual(accepted, [])
        self.assertEqual(
            rejected[0]["verifier_reasons"],
            ["unknown_source_id:NOT-A-SOURCE"],
        )

    def test_missing_evidence_file_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temp_path = Path(temporary_directory)
            for name in ("frame.json", "event.json", "bom.json"):
                source = DEMO_EVIDENCE / name
                (temp_path / name).write_bytes(source.read_bytes())

            with self.assertRaises(EvidenceError):
                build_report(temp_path)

    def test_inconsistent_barcode_event_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temp_path = Path(temporary_directory)
            for name in ("frame.json", "event.json", "bom.json", "sop.json"):
                source = DEMO_EVIDENCE / name
                (temp_path / name).write_bytes(source.read_bytes())

            event_path = temp_path / "event.json"
            event = json.loads(event_path.read_text(encoding="utf-8"))
            event["part_number"] = "CONN-UNKNOWN"
            event_path.write_text(json.dumps(event), encoding="utf-8")

            with self.assertRaises(EvidenceError):
                build_report(temp_path)

    def test_report_is_json_serializable_and_discloses_stage_boundary(self) -> None:
        report = build_report(DEMO_EVIDENCE)
        rendered = json.dumps(report, ensure_ascii=False, sort_keys=True)
        self.assertIn("Stage I deterministic evidence-linking thin slice", rendered)
        self.assertIn("ASUS UGen Intel Arc Pro B70 performance", rendered)


if __name__ == "__main__":
    unittest.main()
