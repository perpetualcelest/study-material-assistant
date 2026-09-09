from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_relevant_paragraphs(paragraphs, query, limit=3):
    if not paragraphs or not query.strip():
        return []

    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
    vectors = vectorizer.fit_transform(paragraphs + [query])

    scores = cosine_similarity(
        vectors[-1],
        vectors[:-1],
    ).flatten()

    ranked = sorted(
        zip(scores, paragraphs),
        key=lambda item: item[0],
        reverse=True,
    )

    results = []

    for score, paragraph in ranked[:limit]:
        if score > 0:
            results.append((paragraph, float(score)))

    return results
