# AI Engineering Lab

Hands-on experiments exploring embeddings, retrieval, and local language-model classification. Each lesson connects a practical question to implementation, observed results, and limitations.

## Read the notebooks

Read the [published lab](https://lakpa.github.io/ai-engineering-lab/) or open the source notebooks in order:

| Notebook | What it explores | Prerequisites |
|---|---|---|
| [01 — Text Embeddings and Semantic Search](embeddings-and-search/01-text-embeddings.ipynb) | Vectors, cosine similarity, and keyword versus semantic song retrieval | Shared Python environment |
| [02 — A Content-Based Song Recommender](embeddings-and-search/02-content-based-recommender.ipynb) | Preference vectors and the limits of text-based recommendations | Shared Python environment |
| [03 — Grounded Recommendation Explanations](embeddings-and-search/03-grounded-recommendation-explanations.ipynb) | Source-linked retrieval and local LLM explanations | Shared Python environment; Ollama with `llama3.2:3b` |
| [04 — Preparing an Intent-Classification Dataset](embeddings-and-search/04-prepare-message-classification-dataset.ipynb) | Label validation, duplicate checks, reproducible splits, and conversation exports | Shared Python environment; no model required |
| [05 — Classifying Messages Locally](embeddings-and-search/05-message-classification-inference.ipynb) | Qwen classification quality and timing with MLX-LM and PyTorch MPS | Run notebook 04 first; Apple Silicon Mac; separate inference environment |

## Run locally

Run the setup commands below from the repository root using Python 3.11. Select the indicated Python interpreter as your notebook kernel and run code cells from top to bottom. The working directory for notebooks 01–03 should be `embeddings-and-search`; notebooks 04–05 also support execution from the repository root.

### Notebooks 01–04: shared environment

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
```

Select `.venv/bin/python` as the kernel. Embedding lessons download `all-MiniLM-L6-v2` on first use and use Chroma in memory.

For notebook 03, install and start [Ollama](https://ollama.com/), then download its generation model:

```sh
ollama pull llama3.2:3b
```

Notebook 04 only prepares data. It does not require Ollama, MLX-LM, a GPU, or a model download.

### Notebook 05: Apple Silicon inference environment

Use a separate environment: the pinned MLX-LM version requires Transformers 5, while the earlier embedding lessons use `sentence-transformers==5.1.2`, which requires Transformers below version 5.

```sh
python3.11 -m venv .venv-inference
.venv-inference/bin/python -m pip install -r requirements-mlx.txt torch==2.14.1 transformers==5.22.1 nbformat==5.10.4 ipykernel==6.29.4
.venv-inference/bin/python -m pip check
```

Switch the kernel to `.venv-inference/bin/python` and restart it before running notebook 05. Continue using `.venv` for notebooks 01–04; do not install the MLX requirements into that shared environment.

The comparison runs as written on an Apple Silicon Mac with MPS support. It downloads a pinned `Qwen/Qwen2.5-0.5B-Instruct` checkpoint on first use (roughly 1 GB). Both workflows then run locally without an Ollama server. Pause other model workloads when collecting timings.

## Data and notebook order

The repository includes the fictional [song dataset](embeddings-and-search/songs.csv), a [public-domain song catalog](embeddings-and-search/public-domain-songs.csv), and [source-linked lyric sections](embeddings-and-search/public-domain-song-lyrics.csv). Classification source messages are in [intentData](embeddings-and-search/intentData).

For classification, generate the local artifacts before running inference:

1. Run every code cell in notebook 04 using `.venv`.
2. Confirm its final counts: **54 training, 6 validation, and 12 evaluation records** with the supplied source data.
3. Switch to `.venv-inference` and run notebook 05.

Notebook 04 writes these paths under `embeddings-and-search/data/`:

| Generated artifact | Purpose |
|---|---|
| `music_service_intents_labeled/` | Saved Hugging Face dataset with class labels and splits |
| `music_service_intents_mlx/train.jsonl` | Training conversations including expected answers |
| `music_service_intents_mlx/valid.jsonl` | Validation conversations including expected answers |
| `music_service_intents_mlx/evaluation.jsonl` | Evaluation inputs with labels stored separately |

These files can be regenerated from the tracked CSVs; a clean checkout need not contain them. Notebook 04 uses seed `42` and a fixed source-file order to reproduce the split from unchanged inputs. Rerunning it rewrites its generated artifacts. Keep source messages, split logic, and evaluation records fixed when comparing model runs, and record the repository commit used. A seed alone does not preserve a dataset if its source changes.

Save notebooks after execution to retain observed results. The 12-example evaluation is a learning exercise, not evidence of production reliability; its existing errors have already been inspected during development.

## Build the website

Install [Quarto](https://quarto.org/docs/get-started/), then run from the repository root:

```sh
quarto render
```

Quarto uses the notebooks' saved outputs by default, so building the site does not require rerunning GPU inference or downloading model weights. Rerun notebooks in their appropriate environments when code or data changes, then save them before rendering. Generated HTML is written to `_site/`.

The [publishing workflow](.github/workflows/quarto-publish.yml) renders the site on pushes to `main` and publishes it to the `gh-pages` branch. GitHub Pages must be configured to deploy from that branch, and Actions needs permission to write repository contents. See [Quarto's GitHub Pages instructions](https://quarto.org/docs/publishing/github-pages.html).

## Check documentation changes

Pull requests run notebook-format validation, README link checks, a Quarto build using saved outputs, and checks for local page and asset targets in the published HTML. These checks do not execute notebooks or download models. External URLs and fragment anchors are not checked.

To run the same checks locally, use a small documentation-only environment with Python 3.11 and Quarto 1.10.18:

```sh
python3.11 -m venv /tmp/ai-lab-docs-checks
/tmp/ai-lab-docs-checks/bin/python -m pip install -r requirements-checks.txt
/tmp/ai-lab-docs-checks/bin/python -m unittest discover -s tests -v
/tmp/ai-lab-docs-checks/bin/python scripts/check_docs.py
quarto render --no-execute
/tmp/ai-lab-docs-checks/bin/python scripts/check_docs.py --site _site
```

Checks cover the sources listed in `_quarto.yml`; unpublished drafts are excluded. Notebook execution and model-quality evaluation remain separate manual steps. The pull-request workflow validates changes without publishing the site.
