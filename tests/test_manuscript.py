import contextlib
import csv
import io
import json
import shutil
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_manuscript import main


class ManuscriptAuditTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.case = Path(tmp.name) / "case"
        shutil.copytree(ROOT / "examples" / "aperture", self.case)
        self.ledger = self.case / "ledger.json"
        self.draft = self.case / "manuscript.md"
        self.csv = self.case / "results.csv"
        self.receipt = self.case / "review.json"

    def check(self, action="check", *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return main([action, str(self.ledger), *map(str, args)])

    def change(self, file, before, after):
        text = file.read_text(encoding="utf-8")
        self.assertIn(before, text)
        file.write_text(text.replace(before, after, 1), encoding="utf-8")

    def test_case_matches_and_all_reported_error_bounds_hold(self):
        self.assertEqual(self.check(), 0)
        with self.csv.open(encoding="utf-8") as stream:
            errors = [abs(Decimal(row["capture"]) - Decimal(row["analytic"]))
                      for row in csv.DictReader(stream) if row["cells"] == "200"]
        self.assertEqual(len(errors), 4)
        self.assertLess(max(errors), Decimal("0.002"))

    def test_wrong_number_in_abstract_despite_correct_results(self):
        self.change(self.draft, "86.47%", "89.47%")
        self.assertEqual(self.check(), 1)

    def test_updated_csv_cell_invalidates_the_original_sentence(self):
        self.change(self.csv, "86.467057517", "85.467057517")
        self.assertEqual(self.check(), 1)

    def test_unit_must_agree(self):
        self.change(self.csv, "86.467057517,%", "86.467057517,mW")
        self.assertEqual(self.check(), 2)

    def test_duplicate_source_rows_fail(self):
        lines = self.csv.read_text().splitlines()
        self.csv.write_text("\n".join(lines + [lines[-1]]) + "\n")
        self.assertEqual(self.check(), 2)

    def test_replaced_figure_target_requires_correction(self):
        self.change(self.draft, "](collection.png)", "](different.png)")
        self.assertEqual(self.check(), 1)

    def test_citation_lacks_bibliography_entry(self):
        self.change(self.draft, "[1] Gao H", "[2] Gao H")
        self.assertEqual(self.check(), 1)

    def test_changed_configuration_stales_existing_receipt(self):
        self.assertEqual(self.check("freeze", "--receipt", self.receipt), 0)
        self.assertEqual(self.check("check", "--receipt", self.receipt), 0)
        self.assertEqual(self.check("freeze", "--receipt", self.receipt), 2)
        with (self.case / "generate.py").open("a", encoding="utf-8") as stream:
            stream.write("\n# Configuration changed\n")
        self.assertEqual(self.check("check", "--receipt", self.receipt), 1)

    def test_new_unregistered_claim_needs_human_review(self):
        with self.draft.open("a", encoding="utf-8") as stream:
            stream.write("这个接收机在所有真实海况下均最优。\n")
        self.assertEqual(self.check(), 0)  # Semantic coverage lies outside a cell-to-text audit.

    def test_no_catalogued_evidence_is_invalid(self):
        self.ledger.write_text(json.dumps({"draft": "manuscript.md", "quantities": [],
                                          "figures": [], "citations": []}))
        self.assertEqual(self.check(), 2)

    def test_reject_input_outside_case(self):
        self.change(self.ledger, '"results.csv"', '"../outside.csv"')
        self.assertEqual(self.check(), 2)


if __name__ == "__main__":
    unittest.main()
