# AI Engineering Lab

Hands-on notebooks documenting my AI engineering experiments with embeddings, vector search, and retrieval.

## Read the notebooks

- [Text Embeddings and Semantic Search](embeddings-and-search/01-text-embeddings.ipynb) explains vectors and cosine similarity, builds a song search engine, and compares keyword and semantic retrieval.

The notebook uses the fictional [song dataset](embeddings-and-search/songs.csv), Chroma in memory, and the `all-MiniLM-L6-v2` model.

## Run locally

Create a Python environment, install the packages in `requirements.txt`, and select that environment as the Jupyter kernel. Run the notebook cells from top to bottom. The first notebook reads `songs.csv` relative to the `embeddings-and-search` directory.

To render the Quarto site, install [Quarto](https://quarto.org/docs/get-started/) and run `quarto render` from the repository root. Quarto uses the notebooks' saved outputs by default; rerun cells in Jupyter after changing code or data so the article reflects the current results.

The [publishing workflow](.github/workflows/quarto-publish.yml) renders the site on pushes to `main` and publishes it to the `gh-pages` branch. GitHub Pages must be configured to deploy from that branch, and Actions needs permission to write repository contents. See [Quarto's GitHub Pages instructions](https://quarto.org/docs/publishing/github-pages.html).
