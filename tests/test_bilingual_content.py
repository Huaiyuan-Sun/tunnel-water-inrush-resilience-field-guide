"""双语内容与现场表单结构测试。 / Bilingual-content and form-structure tests."""

import csv
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MARKER = '<a id="english-version"></a>'


class BilingualContentTests(unittest.TestCase):
    def test_every_markdown_file_is_chinese_first_and_english_second(self):
        markdown_files = sorted(ROOT.rglob("*.md"))
        self.assertTrue(markdown_files)
        for path in markdown_files:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertEqual(text.count(MARKER), 1)
                chinese, english = text.split(MARKER)
                self.assertRegex(chinese, r"[\u4e00-\u9fff]")
                self.assertRegex(english, r"[A-Za-z]{4,}")
                self.assertLess(
                    text.find(next(char for char in text if "\u4e00" <= char <= "\u9fff")),
                    text.find(MARKER),
                )

    def test_csv_files_have_stable_keys_and_bilingual_label_row(self):
        csv_files = sorted(ROOT.rglob("*.csv"))
        self.assertTrue(csv_files)
        for path in csv_files:
            with path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle))
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertGreaterEqual(len(rows), 2)
                self.assertEqual(len(rows[0]), len(rows[1]))
                self.assertTrue(all("/" in cell for cell in rows[1]))
                self.assertTrue(any(any("\u4e00" <= c <= "\u9fff" for c in cell) for cell in rows[1]))
                self.assertTrue(any(any(c.isascii() and c.isalpha() for c in cell) for cell in rows[1]))
                for row in rows[2:]:
                    self.assertEqual(len(row), len(rows[0]))

    def test_example_json_has_bilingual_note(self):
        payload = json.loads(
            (ROOT / "examples" / "example-assessment.json").read_text(encoding="utf-8")
        )
        self.assertIn("_说明_zh", payload)
        self.assertIn("_note_en", payload)


if __name__ == "__main__":
    unittest.main()
