# SHL Assessment Recommendation System

This project is a Retrieval-Augmented Generation (RAG)-based tool designed to help recruiters and hiring managers find the most relevant SHL assessments for their specific job requirements using natural language queries.

---

## Project Components

### 1. Web Scraping (`data_scrape.py`)
- Uses `Selenium`, `BeautifulSoup`, and `requests` to scrape SHL’s assessment catalog.
- Extracts details like Test Name, Link, Remote Testing, Adaptive/IRT, Test Type, and Duration.
- Saves raw data into `final_data.csv`.

### 2. Preprocessing(`explore.ipynb`)
- Cleans the scraped data (e.g., maps Test Type codes like `C`, `A` to full forms like `Cognitive`, `Aptitude`, etc.).
- Removes "minutes" from the Duration field.
- Saves cleaned dataset into `final_data_cleaned.csv`.

### 3. Embedding + Indexing (`embedding.py`)
- Uses the SentenceTransformer model `multi-qa-mpnet-base-dot-v1` to create semantic embeddings.
- Stores the embeddings in a FAISS index (`shl_faiss3.index`) for fast retrieval.
- Saves a mapping to the original records (`shl_index_mapping3.pkl`).

### 4. Backend API (`main.py`)
- Built with FastAPI.
- Loads the FAISS index and returns the top-10 most relevant assessments for a given query.
- Hosted via Render and exposed at `/recommend`.

### 5. Streamlit UI (`app.py`)
- Provides a simple web interface for users to input job descriptions.
- Sends queries to the FastAPI backend and displays matching assessments.

### 6. Evaluation (`evaluation.py`)
- Implements standard metrics such as Recall@k and MAP@k to evaluate retrieval performance.
- Reads `evaluation_data.json` to compare model output against ground truth
- **Recall@k**: Measures how many relevant assessments appear in the top-k results.
- **MAP@k (Mean Average Precision)**: Measures the average precision of relevant assessments, rewarding correct ranking within the top-k.
- Recall@1:  0.1444
-Recall@5:  0.5222
-MAP@1:     1.0000
-MAP@5:     0.8500


---

##  Deployment Links

- **Live App (Frontend)**: [Streamlit App](https://shl-assessment-app.streamlit.app)
- **API Endpoint**: [FastAPI `/recommend`](https://shl-task-qz8g.onrender.com/recommend)
- **GitHub Codebase**: [GitHub Repository](https://github.com/karthikeya100804/shl_task)

---
##  Setup Instructions (For Local Use)
```
git clone https://github.com/karthikeya100804/shl_task.git
cd shl_task
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Libraries Used

- `selenium`, `beautifulsoup4`, `requests`, `pandas`, `re`
- `sentence-transformers`, `faiss-cpu`, `pickle`, `numpy`
- `fastapi`, `uvicorn`, `python-dotenv`, `google-generativeai`
- `streamlit`

---

##  Files Included

- `data_scrape.py` – Web scraping
- `embedding.py` – Embedding and indexing
- `main.py` – FastAPI backend
- `app.py` – Streamlit frontend
- `evaluation.py`, `evaluation_data.json` – Performance evaluation
- `final_data_cleaned.csv` – Cleaned dataset
- `shl_faiss3.index`, `shl_index_mapping3.pkl` – Index and mapping
- `requirements.txt`, `Procfile`, `.gitignore`

---

##  Notes

- Backend is hosted via [Render](https://render.com), frontend via [Streamlit Community Cloud](https://streamlit.io/).
- API follows query interface described in the assignment documentation (Appendix 2).
- Evaluation is done using real queries and known ground truth results.

---

