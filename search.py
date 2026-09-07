from pathlib import Path
def load_notes():
    note_texts = []

    for file_path in Path("data").glob("*.txt"):
        note_texts.append(file_path.read_text(encoding="utf-8"))

    return "\n\n".join(note_texts)
def find_matching_paragraphs(text, keyword):
    results = []

    for paragraph in text.split("\n\n"):
        if keyword in paragraph.lower():
            results.append(paragraph)

    return results

text = load_notes()

while True:
    keyword = input("请输入关键词（输入 q 退出）：").strip().lower()

    if keyword == "q":
        print("程序已退出。")
        break

    if keyword == "":
        print("关键词不能为空。")
        continue

    paragraphs = find_matching_paragraphs(text, keyword)

    if paragraphs:
        print("找到了相关内容：")

        for paragraph in paragraphs:
            print(paragraph)
    else:
        print("没有找到相关内容。")