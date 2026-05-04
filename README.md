# MovieBuddy

Pick a movie you love and get 5 similar ones instantly — deployed on Streamlit Community Cloud.

## Live Demo

**[Try MovieBuddy →](https://your-app-url.streamlit.app)** *(update with your Streamlit URL)*

> *Screenshot placeholder — dropdown selector on the left, recommendation table with % match on the right*

---

## What it solves

Deciding what to watch next is harder than it should be. MovieBuddy gives you 5 content-based recommendations the moment you pick a movie — no account, no ratings history, no cold-start problem. Just metadata similarity.

---

## How it works

The system is content-based: it recommends movies that share similar metadata, not user behaviour.

**Preprocessing (offline):**
1. Merge TMDB movies + credits datasets (4,509 English-language films)
2. Extract genres, keywords, top-3 cast, and director from JSON columns
3. Concatenate into a single `tag` string per movie
4. Lowercase + Porter stemming (so "running", "ran", "runs" → "run")
5. Vectorize with `CountVectorizer` (5,000 features, English stop words removed)
6. Compute pairwise cosine similarity for all 4,509 movies → saved to `cv_similarity_f.pkl`

**At query time:**
- User selects a movie from the dropdown
- App looks up the precomputed similarity row for that movie
- Sorts all other movies by score, returns top 5 with percentage match

Six vectorizers were tested during development: CountVectorizer (unlimited, 5000, 3000 features), TF-IDF (unlimited, 5000 features), and Word2Vec (gensim). Word2Vec collapsed — it produced near-identical similarity scores (~99.6%) across all movies, making it unusable for recommendations. CountVectorizer with 3000–5000 features gave the best qualitative results and was selected for production.

---

## Tech stack

| Layer | Tool |
|---|---|
| Data processing | Pandas, NLTK (Porter Stemmer) |
| Vectorization | Scikit-learn CountVectorizer |
| Similarity | Scikit-learn cosine_similarity |
| UI | Streamlit |
| Dataset | [TMDB 5000 Movies](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) (Kaggle) |

---

## Run it locally

```bash
git clone https://github.com/huzefa10/movie-recommender_deploy.git
cd movie-recommender_deploy

pip install -r requirements.txt

streamlit run app.py
```

Open `http://localhost:8501`, pick a movie, click **Get Movies**.

> The similarity matrix (`cv_similarity_f.pkl`, ~78 MB) is already included in the repo so no preprocessing step is needed.

---

## Project structure

```
movie-recommender_deploy/
├── app.py                  # Streamlit app
├── mov_df.csv              # Processed movie titles (used at runtime)
├── new_df.csv              # Full processed dataset with tags
├── cv_similarity_f.pkl     # Precomputed cosine similarity matrix
└── requirements.txt        # Dependencies
```

---

## Future improvements

- Add TMDB poster images to recommendations
- Try approximate nearest-neighbor search (Annoy / FAISS) to avoid storing the full similarity matrix
- Experiment with sentence embeddings (SBERT) for richer semantic matching
- Add genre filter to constrain recommendations within a category
