from pathlib import Path

from llm import generate_answer
from notes import load_paragraphs
from prompt_builder import build_prompt
from semantic_retrieval import embed_texts, find_semantic_paragraphs

all_paragraphs = load_paragraphs(Path("data"))

paragraph_texts = [
    paragraph for paragraph, source in all_paragraphs
]

print("正在建立资料向量索引，请稍候……")
paragraph_vectors = embed_texts(paragraph_texts)
print("资料向量索引建立完成。")

while True:
    keyword = input("请输入问题（输入 q 退出）：").strip().lower()
    if keyword == "q":
        print("程序已退出。")
        break

    if keyword == "":
        print("问题不能为空。")
        continue

    results = find_semantic_paragraphs(
        all_paragraphs,
        keyword,
        paragraph_vectors=paragraph_vectors,
    )

    if results:
        print("找到了相关内容：")

        for paragraph, score, source in results:
            print(f"来源：{source}")
            print(f"相关度：{score:.2f}")
            print(paragraph)

        relevant_paragraphs = [
            f"[来源：{source}]\n{paragraph}"
            for paragraph, score, source in results
        ]
        prompt = build_prompt(relevant_paragraphs, keyword)

        print("\n准备交给大模型的提示词：")
        print(prompt)

        print("\n正在生成答案，请稍候……")
        answer = generate_answer(prompt)

        print("\n大模型回答：")
        print(answer)

        sources = []

        for paragraph, score, source in results:
            if source not in sources:
                sources.append(source)

        print("\n参考资料：")

        for source in sources:
            print(f"- {source}")
    else:
        print("没有找到相关内容。")
