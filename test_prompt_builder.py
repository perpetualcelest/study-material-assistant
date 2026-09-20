import unittest

from prompt_builder import build_prompt


class TestBuildPrompt(unittest.TestCase):
    def test_builds_prompt_with_context_and_question(self):
        paragraphs = [
            "机器学习让计算机从数据中学习规律。",
            "RAG 会先检索资料，再生成答案。",
        ]

        prompt = build_prompt(paragraphs, "什么是 RAG？")

        self.assertIn("RAG 会先检索资料，再生成答案。", prompt)
        self.assertIn("什么是 RAG？", prompt)
    def test_requires_answer_to_be_based_on_context(self):
        prompt = build_prompt(
            ["Python 是一种编程语言。"],
            "Python 是谁发明的？",
        )

        self.assertIn("只能根据资料回答", prompt)
        self.assertIn("资料中没有足够信息", prompt)

if __name__ == "__main__":
    unittest.main()