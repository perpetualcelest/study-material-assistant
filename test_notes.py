import unittest
from pathlib import Path

from notes import load_paragraphs, split_text


class NotesTest(unittest.TestCase):
    def test_loads_paragraphs_with_source_names(self):
        paragraphs = load_paragraphs(Path("data"))

        sources = [
            source for text, source in paragraphs
        ]

        self.assertIn("ai.txt", sources)
        self.assertIn("notes.txt", sources)

     def test_splits_text_with_overlap(self):
        chunks = split_text(
            "ABCDEFGHIJKL",
            chunk_size=6,
            overlap=2,
        )

        self.assertEqual(
            chunks,
            ["ABCDEF", "EFGHIJ", "IJKL"],
        )


if __name__ == "__main__":
    unittest.main() 