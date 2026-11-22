import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_tex_edit import check


class TexEditTests(unittest.TestCase):
    def setUp(self):
        case = ROOT / "examples" / "aperture"
        self.original = (case / "original-en.tex").read_text(encoding="utf-8")
        self.final = (case / "edited-en.tex").read_text(encoding="utf-8")
        self.phrases = ["centered aperture", "four radii tested", "percentage points"]

    def test_corrected_english(self):
        self.assertEqual(check(self.original, self.final, self.phrases), [])

    def test_rejects_each_material_change(self):
        pairs = [("86.47", "89.47"), ("$a=w$", "$a=2w$"), (r"\cite{Gao2025}", r"\cite{Gao2026}"),
                 ("four radii tested", "all radii"), ("percentage points", "percent")]
        for old, new in pairs:
            with self.subTest(old=old):
                self.assertTrue(check(self.original, self.final.replace(old, new), self.phrases))

    def test_unregistered_semantic_change_needs_reader(self):
        changed = self.final.replace("cannot identify", "can identify")
        self.assertEqual(check(self.original, changed, self.phrases), [])

    def test_display_math_and_signed_units(self):
        original = r"Measured at -40 dBm. \[P=I_0A\] \eqref{eq:power}"
        for key, replacement in [("-40 dBm", "40 dBm"), ("dBm", "mW"),
                                 ("I_0A", "I_1A"), ("eq:power", "eq:power2")]:
            with self.subTest(key=key):
                self.assertTrue(check(original, original.replace(key, replacement), []))

    def test_macro_and_unmatched_math_require_separate_inspection(self):
        for text in [r"\input{body}", r"Use $a=1 without a closing delimiter."]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                check(text, text, [])


if __name__ == "__main__":
    unittest.main()
