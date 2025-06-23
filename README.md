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
   git clone <repo-url>
   cd NonprofitResourcesChatbot
   ```
2. (Optional) Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Run the chatbot:
   ```powershell
   python main.py
   ```

## Usage
- Interact with the chatbot to find nonprofit resources based on your needs.
- Use the Jupyter notebook for data processing and embedding if you wish to update or expand the dataset.

## License
This project is intended for educational and nonprofit use.

---
Feel free to contribute or open issues for suggestions and improvements.
