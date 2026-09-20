def build_prompt(paragraphs, question):
    context = "\n".join(paragraphs)

    return (
        "你是一个学习资料问答助手。\n"
        "只能根据资料回答，不要使用资料之外的知识。\n"
        "如果资料中没有足够信息，请回答：资料中没有足够信息。\n"
        "请直接给出简洁答案。\n\n"
        f"资料：\n{context}\n\n"
        f"问题：{question}\n"
        "答案："
    )