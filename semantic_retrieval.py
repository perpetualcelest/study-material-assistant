import json
from urllib.request import Request, urlopen

from sklearn.metrics.pairwise import cosine_similarity


def find_semantic_paragraphs(
    paragraphs,
    query,
    limit=3,
    min_score=0.48,
):
    if not paragraphs or not query.strip():
        return []

    texts = [text for text, source in paragraphs]
    body = json.dumps({
        "model": "bge-m3",
        "input": texts + [query],
    }).encode("utf-8")

    request = Request(
        "http://localhost:11434/api/embed",
        data=body,
        headers={"Content-Type": "application/json"},
    )

    with urlopen(request) as response:
        vectors = json.load(response)["embeddings"]

    scores = cosine_similarity(
        [vectors[-1]],
        vectors[:-1],
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
