import unittest

from retrieval import find_relevant_paragraphs


class RetrievalTest(unittest.TestCase):
    def test_machine_learning_paragraph_ranks_first(self):
        paragraphs = [
            "Python 是一种编程语言。",
            "机器学习让计算机从数据中学习规律。",
            "今天天气很好。",
        ]

        results = find_relevant_paragraphs(paragraphs, "机器学习")

        self.assertEqual(results[0][0], paragraphs[1])
        self.assertGreater(results[0][1], 0)


if __name__ == "__main__":
    unittest.main()
