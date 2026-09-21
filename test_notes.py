import unittest
from pathlib import Path

from notes import load_paragraphs


class NotesTest(unittest.TestCase):
    def test_loads_paragraphs_with_source_names(self):
        paragraphs = load_paragraphs(Path("data"))

        sources = [
            source for text, source in paragraphs
        ]

        self.assertIn("ai.txt", sources)
        self.assertIn("notes.txt", sources)


if __name__ == "__main__":
    unittest.main() 