def split_text(text, chunk_size=500, overlap=50):
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 必须大于等于 0，并且小于 chunk_size")

    step = chunk_size - overlap

    return [
        text[start:start + chunk_size]
        for start in range(0, len(text), step)
    ]
def load_paragraphs(data_directory):
    paragraphs = []

    for file_path in data_directory.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        for paragraph in text.split("\n\n"):
            paragraph = paragraph.strip()

                       if paragraph:
                chunks = split_text(paragraph)

                for chunk in chunks:
                    paragraphs.append((chunk, file_path.name))

    return paragraphs