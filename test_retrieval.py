import unittest

from retrieval import find_relevant_paragraphs


class RetrievalTest(unittest.TestCase):
    def test_machine_learning_paragraph_ranks_first(self):
        paragraphs = [
            ("Python 是一种编程语言。", "notes.txt"),
            ("机器学习让计算机从数据中学习规律。", "ai.txt"),
            ("今天天气很好。", "notes.txt"),
        ]

        results = find_relevant_paragraphs(paragraphs, "机器学习")

        self.assertEqual(results[0][0], paragraphs[1][0])
        self.assertGreater(results[0][1], 0)
        self.assertEqual(results[0][2], "ai.txt")

    def test_filters_low_relevance_paragraphs(self):
        paragraphs = [
            ("机器学习是让计算机从数据中学习规律。", "ai.txt"),
            ("机器学习是人工智能的一种方法。", "ai.txt"),
            (
                "大语言模型可以根据大量文本学习语言规律，并生成新的文字。",
                "notes.txt",
            ),
        ]

        results = find_relevant_paragraphs(
            paragraphs,
            "什么是机器学习",
        )

        result_paragraphs = [
            paragraph for paragraph, score, source in results
        ]

        self.assertNotIn(paragraphs[2][0], result_paragraphs)


if __name__ == "__main__":
    unittest.main()