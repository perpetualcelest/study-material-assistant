from pathlib import Path

from retrieval import find_relevant_paragraphs


def load_notes():
    note_texts = []

    for file_path in Path("data").glob("*.txt"):
        note_texts.append(file_path.read_text(encoding="utf-8"))

    return "\n\n".join(note_texts)

text = load_notes()
all_paragraphs = []

for paragraph in text.split("\n\n"):
    paragraph = paragraph.strip()

    if paragraph:
        all_paragraphs.append(paragraph)

while True:
    keyword = input("请输入问题（输入 q 退出）：").strip().lower()

    if keyword == "q":
        print("程序已退出。")
        break

    if keyword == "":
        print("问题不能为空。")
        continue

    results = find_relevant_paragraphs(all_paragraphs, keyword)

    if results:
        print("找到了相关内容：")

        for paragraph, score in results:
            print(f"相关度：{score:.2f}")
            print(paragraph)
    else:
        print("没有找到相关内容。")
