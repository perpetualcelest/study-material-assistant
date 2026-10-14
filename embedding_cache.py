import json

from semantic_retrieval import embed_texts


def load_or_create_vectors(texts, cache_path):
    if cache_path.exists():
        saved = json.loads(cache_path.read_text(encoding="utf-8"))

        if saved["texts"] == texts:
            return saved["vectors"]

    vectors = embed_texts(texts)

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps({"texts": texts, "vectors": vectors}),
        encoding="utf-8",
    )

    return vectors