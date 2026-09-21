def load_paragraphs(data_directory):
    paragraphs = []

    for file_path in data_directory.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        for paragraph in text.split("\n\n"):
            paragraph = paragraph.strip()

            if paragraph:
                paragraphs.append((paragraph, file_path.name))

    return paragraphs