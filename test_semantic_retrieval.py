import unittest

from semantic_retrieval import embed_texts, find_semantic_paragraphs


class SemanticRetrievalTest(unittest.TestCase):
    def test_embeds_each_input_text(self):
        vectors = embed_texts([
            "机器学习",
            "人工智能",
        ])

        self.assertEqual(len(vectors), 2)
        self.assertGreater(len(vectors[0]), 0)

    def test_ranks_similar_meaning_first(self):
        paragraphs = [
            ("今天晚餐吃米饭。", "food.txt"),
            ("汽车在公路上行驶。", "traffic.txt"),
        ]

        results = find_semantic_paragraphs(
            paragraphs,
            "机动车在道路上行驶",
        )

        self.assertEqual(results[0][0], "汽车在公路上行驶。")
        self.assertEqual(results[0][2], "traffic.txt")

    def test_filters_scores_below_minimum(self):
        paragraphs = [
            ("汽车在公路上行驶。", "traffic.txt"),
            ("今天晚餐吃米饭。", "food.txt"),
        ]

        results = find_semantic_paragraphs(
            paragraphs,
            "机动车在道路上行驶",
            min_score=0.6,
        )

        result_paragraphs = [
            paragraph for paragraph, score, source in results
        ]

        self.assertEqual(
            result_paragraphs,
            ["汽车在公路上行驶。"],
        )

    def test_uses_precomputed_paragraph_vectors(self):
        paragraphs = [
            ("今天晚餐吃米饭。", "food.txt"),
            ("汽车在公路上行驶。", "traffic.txt"),
        ]

        paragraph_vectors = embed_texts([
            paragraph for paragraph, source in paragraphs
        ])

        results = find_semantic_paragraphs(
            paragraphs,
            "机动车在道路上行驶",
            paragraph_vectors=paragraph_vectors,
        )

        self.assertEqual(
            results[0][0],
            "汽车在公路上行驶。",
        )


if __name__ == "__main__":
    unittest.main()
