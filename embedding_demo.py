import json
from urllib.request import Request, urlopen
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity


texts = [
    "汽车在公路上行驶",
    "机动车在道路上行驶",
    "今天晚餐吃米饭",
]

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
    embeddings = json.load(response)["embeddings"]

scores = cosine_similarity(embeddings)[0]

print("Embedding 结果：")
for text, score in zip(texts, scores):
    print(f"{score:.3f}  {text}")

vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
tfidf_vectors = vectorizer.fit_transform(texts)
tfidf_scores = cosine_similarity(tfidf_vectors)[0]

print("\nTF-IDF 结果：")
for text, score in zip(texts, tfidf_scores):
    print(f"{score:.3f}  {text}")