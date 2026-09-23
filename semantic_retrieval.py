import json
from urllib.request import Request, urlopen

from sklearn.metrics.pairwise import cosine_similarity


def embed_texts(texts):
    body = json.dumps({
        "model": "bge-m3",
        "input": texts,
    }).encode("utf-8")

    request = Request(
        "http://localhost:11434/api/embed",
        data=body,
        headers={"Content-Type": "application/json"},
    )

    with urlopen(request) as response:
        return json.load(response)["embeddings"]


def find_semantic_paragraphs(
    paragraphs,
    query,
    limit=3,
    min_score=0.48,
    paragraph_vectors=None,
):
    if not paragraphs or not query.strip():
        return []

    texts = [text for text, source in paragraphs]

    if paragraph_vectors is None:
        vectors = embed_texts(texts + [query])
        paragraph_vectors = vectors[:-1]
        query_vector = vectors[-1]
    else:
        query_vector = embed_texts([query])[0]

    scores = cosine_similarity(
        [query_vector],
        paragraph_vectors,
    )[0]

    ranked = sorted(
        zip(scores, paragraphs),
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        (text, float(score), source)
        for score, (text, source) in ranked[:limit]
        if score >= min_score
    ]
