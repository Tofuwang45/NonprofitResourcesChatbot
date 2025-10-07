# Nonprofit Resources Chatbot

This repository contains a chatbot project designed to help users find and access resources for nonprofits. The chatbot leverages data from CSV files and uses embeddings to provide relevant information and recommendations.

## Features
- Processes and embeds nonprofit resource data for efficient search and retrieval
- Provides a conversational interface to help users discover nonprofit resources
- Includes scripts for data scraping, embedding, and chatbot logic

## Repository Structure
- `main.py` — Main script for running the chatbot
- `scrape_embed.ipynb` — Jupyter notebook for scraping and embedding data
- `all_nonprofits.csv` — Main dataset of nonprofit resources
- `smlist.csv` — Supplementary data
- `summary_embeddings.npy` — Precomputed embeddings for fast similarity search

## Requirements
- Python 3.12 or later
- Recommended: Create and activate a virtual environment
- Required packages (install via pip):
  - numpy
  - pandas
  - (other packages as needed by your code)

## Getting Started
1. Clone this repository:
   ```powershell
   # Nonprofit Resources Chatbot

   This repository contains a chatbot that helps users find nonprofit resources. It uses precomputed embeddings and a small semantic search pipeline to return relevant nonprofit records from the included CSVs.

   ## What's included
   - `main.py` — Core search and message-processing logic (language detection, translation, SBERT embeddings, similarity search)
   - `api.py` — FastAPI wrapper around `main.py` (serves the web frontend)
   - `chatbot-frontend/` — Vite + TypeScript React frontend
   - `all_nonprofits.csv`, `smlist.csv` — datasets
   - `summary_embeddings.npy` — precomputed embeddings for fast similarity search

   ## Requirements
   - Python 3.11+ recommended (works with 3.12)
   - Node.js + npm for the frontend
   - Install Python packages:

      pip install -r requirements.txt

   Notes on heavy dependencies
   - `sentence-transformers` and `torch` will download models on first use; allow extra time.
   - The `requirements.txt` pins CPU-only `torch`. If you have a CUDA-capable GPU, follow the instructions at https://pytorch.org/get-started/locally/ to install the matching `torch` wheel for your CUDA version.
   - Install the spaCy language models used by the project:

      python -m spacy download en_core_web_sm
      python -m spacy download es_core_news_sm

   ## Running locally (backend + frontend)

   1. (Optional) Create and activate a virtual environment

      python -m venv venv
      .\venv\Scripts\Activate

   2. Install Python dependencies

      pip install -r requirements.txt

   3. Start the backend API (this imports `main.py` and may take time while models load)

      python api.py

   Environment variables you can set to tune timeouts (helpful on slower machines):

   - `IMPORT_TIMEOUT` — seconds to wait for the heavy `main` import at startup (default 120)
   - `REQUEST_TIMEOUT` — seconds to allow for a single search request (default 60)

   Example (PowerShell):

      $env:IMPORT_TIMEOUT = "180"
      $env:REQUEST_TIMEOUT = "120"
      python api.py

   4. Start the frontend (in a separate terminal)

      cd chatbot-frontend
      npm install
      npm run dev

   The Vite dev server proxies `/api/*` requests to `http://127.0.0.1:8000` by default.

   ## Troubleshooting

   - If `api.py` returns a health response with `backend_loaded: false`, check the `import_error` field. Large models (SBERT, spaCy) may take a minute or two to download and initialize.
   - If you see `ModuleNotFoundError` for packages like `langdetect` or `spacy`, ensure you ran `pip install -r requirements.txt` inside the activated venv.
   - If embeddings or CSVs are missing, `main.py` will not be able to perform searches. Make sure `summary_embeddings.npy` and `all_nonprofits.csv` are present in the repository root.

   ## Development notes

   - The API endpoint is `POST /api/chat` and expects JSON: `{ "message": "...", "top_k": 5 }`. It returns a JSON object with `results` (array) and `language`.
   - The frontend is located in `chatbot-frontend/` and uses React + TypeScript with `react-icons` for small UI affordances.

   ## Contributing

   Feel free to open issues or submit PRs. Small improvements that help reliability (tests, CI, pinned deps) are welcome.

   ---

   ```
