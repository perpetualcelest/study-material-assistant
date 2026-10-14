import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from embedding_cache import load_or_create_vectors


class EmbeddingCacheTest(unittest.TestCase):
    def test_reuses_saved_vectors(self):
        with TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "embeddings.json"

            with patch("embedding_cache.embed_texts", return_value=[[1.0]]) as embed:
                first = load_or_create_vectors(["机器学习"], cache_path)
                second = load_or_create_vectors(["机器学习"], cache_path)

            self.assertEqual(first, second)
            self.assertEqual(embed.call_count, 1)

    def test_recalculates_when_texts_change(self):
        with TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "embeddings.json"

            with patch("embedding_cache.embed_texts", side_effect=[[[1.0]], [[2.0]]]) as embed:
                load_or_create_vectors(["机器学习"], cache_path)
                updated = load_or_create_vectors(["人工智能"], cache_path)

            self.assertEqual(updated, [[2.0]])
            self.assertEqual(embed.call_count, 2)


if __name__ == "__main__":
    unittest.main()
