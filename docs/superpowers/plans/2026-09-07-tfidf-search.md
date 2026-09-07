# TF-IDF Search Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace exact keyword matching with TF-IDF ranking that returns at most three relevant paragraphs.

**Architecture:** Keep file loading and the interactive loop in `search.py`. Put the reusable TF-IDF ranking function in `retrieval.py`, allowing one small standard-library test to import it without starting the interactive program.

**Tech Stack:** Python 3.11, scikit-learn 1.7.2, standard-library `unittest`

---

### Task 1: Build and test the TF-IDF ranking function

**Files:**
- Create: `test_retrieval.py`
- Create: `retrieval.py`

- [ ] **Step 1: Write the failing test**

Create `test_retrieval.py`:

```python
import unittest

from retrieval import find_relevant_paragraphs


class RetrievalTest(unittest.TestCase):
    def test_machine_learning_paragraph_ranks_first(self):
        paragraphs = [
            "Python 是一种编程语言。",
            "机器学习让计算机从数据中学习规律。",
            "今天天气很好。",
        ]

        results = find_relevant_paragraphs(paragraphs, "机器学习")

        self.assertEqual(results[0][0], paragraphs[1])
        self.assertGreater(results[0][1], 0)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify the expected failure**

Run:

```powershell
python -m unittest test_retrieval.py -v
```

Expected: `ERROR` containing `ModuleNotFoundError: No module named 'retrieval'` because `retrieval.py` does not exist yet.

- [ ] **Step 3: Add the minimal implementation**

Create `retrieval.py`:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_relevant_paragraphs(paragraphs, query, limit=3):
    if not paragraphs or not query.strip():
        return []

    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
    vectors = vectorizer.fit_transform(paragraphs + [query])
    scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
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
```

`analyzer="char"` is intentional: Chinese text usually has no spaces, so character groups work better here than scikit-learn's default word splitting.

- [ ] **Step 4: Run the test and verify it passes**

Run:

```powershell
python -m unittest test_retrieval.py -v
```

Expected: one test reports `ok`, followed by `OK`.

### Task 2: Connect TF-IDF ranking to the interactive program

**Files:**
- Modify: `search.py`

- [ ] **Step 1: Import the new ranking function**

Add below the `pathlib` import:

```python
from retrieval import find_relevant_paragraphs
```

- [ ] **Step 2: Remove the old exact-match function**

Delete the complete `find_matching_paragraphs` function. It is replaced by `find_relevant_paragraphs`.

- [ ] **Step 3: Split loaded text into clean paragraphs once**

Replace:

```python
text = load_notes()
```

with:

```python
text = load_notes()
paragraphs = []

for paragraph in text.split("\n\n"):
    paragraph = paragraph.strip()
    if paragraph:
        paragraphs.append(paragraph)
```

- [ ] **Step 4: Use ranked results inside the input loop**

Replace:

```python
paragraphs = find_matching_paragraphs(text, keyword)

if paragraphs:
    print("找到了相关内容：")

    for paragraph in paragraphs:
        print(paragraph)
else:
    print("没有找到相关内容。")
```

with:

```python
results = find_relevant_paragraphs(paragraphs, keyword)

if results:
    print("找到了相关内容：")

    for paragraph, score in results:
        print(f"相关度：{score:.2f}")
        print(paragraph)
else:
    print("没有找到相关内容。")
```

- [ ] **Step 5: Run the existing test again**

Run:

```powershell
python -m unittest test_retrieval.py -v
```

Expected: one test reports `ok`, followed by `OK`.

- [ ] **Step 6: Smoke-test the interactive program**

Run:

```powershell
python search.py
```

Enter `机器学习`, then `q`.

Expected: up to three paragraphs are shown from highest to lowest relevance, each with a score greater than zero; entering `q` exits normally.

### Task 3: Record the dependency

**Files:**
- Create: `requirements.txt`

- [ ] **Step 1: Add the installed direct dependency**

Create `requirements.txt`:

```text
scikit-learn==1.7.2
```

- [ ] **Step 2: Verify installation from the dependency file**

Run:

```powershell
python -m pip install -r requirements.txt
```

Expected: scikit-learn is already satisfied and the command exits successfully.

- [ ] **Step 3: Run the complete check**

Run:

```powershell
python -m unittest test_retrieval.py -v
```

Expected: one test reports `ok`, followed by `OK`.

The folder is not a Git repository yet, so commits are intentionally deferred until the Git lesson.
