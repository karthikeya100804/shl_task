from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ========== SETUP ==========
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
llm = genai.GenerativeModel(model_name="gemini-pro")

app = FastAPI()

# Allow Streamlit or browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ========== LOAD FAISS + MAPPING ==========
faiss_index = faiss.read_index("./shl_faiss3.index")
with open("./shl_index_mapping3.pkl", "rb") as f:
    record_mapping = pickle.load(f)

embedder = SentenceTransformer("multi-qa-mpnet-base-dot-v1")

# ========== ROUTES ==========
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recommend")
def recommend(text: str = Query(..., description="Enter job description or query")):
    # Embed the query
    query_vec = embedder.encode([text])
    
    # Search in FAISS
    top_k = 10
    scores, indices = faiss_index.search(np.array(query_vec).astype('float32'), top_k)

    # Retrieve top-k records from mapping
    results = []
    for idx in indices[0]:
        record = record_mapping[idx]
        record["text"] = f"""
Assessment Name: {record['Test Name']}
Test Type: {record['Test Type']}
Remote Testing: {record['Remote Testing']}
Adaptive/IRT: {record['Adaptive/IRT']}
Duration: {record['Duration (min)']} minutes
URL: {record['Test Link']}
"""
        results.append(record)

    return {
        "query": text,
        "results": results
    }
