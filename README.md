# AI Engineering Lab

Hands-on notebooks documenting my AI engineering experiments with embeddings, vector search, and retrieval.

## Read the notebooks

- [Text Embeddings and Semantic Search](embeddings-and-search/01-text-embeddings.ipynb) explains vectors and cosine similarity, builds a song search engine, and compares keyword and semantic retrieval.
- [A Content-Based Song Recommender](embeddings-and-search/02-content-based-recommender.ipynb) averages embeddings of three liked songs, recommends unheard songs, and inspects where text similarity falls short.
- [Grounded Recommendation Explanations](embeddings-and-search/03-grounded-recommendation-explanations.ipynb) retrieves source-linked song evidence and uses Llama 3.2 to explain strong and weak recommendations.

The first two notebooks use the fictional [song dataset](embeddings-and-search/songs.csv). The RAG explanation notebook uses a separate [public-domain song catalog](embeddings-and-search/public-domain-songs.csv) with [source-linked lyric sections](embeddings-and-search/public-domain-song-lyrics.csv). The examples use Chroma in memory and the `all-MiniLM-L6-v2` model.

## Run locally

Create a project environment and install the notebook dependencies:

```sh
python3.10 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
```

Select `.venv/bin/python` as the Jupyter kernel. Run each notebook's cells from top to bottom. Notebooks that load `songs.csv` expect the working directory to be `embeddings-and-search`.

To render the Quarto site, install [Quarto](https://quarto.org/docs/get-started/) and run `quarto render` from the repository root. Quarto uses the notebooks' saved outputs by default; rerun cells in Jupyter after changing code or data so the article reflects the current results.

The [publishing workflow](.github/workflows/quarto-publish.yml) renders the site on pushes to `main` and publishes it to the `gh-pages` branch. GitHub Pages must be configured to deploy from that branch, and Actions needs permission to write repository contents. See [Quarto's GitHub Pages instructions](https://quarto.org/docs/publishing/github-pages.html).
