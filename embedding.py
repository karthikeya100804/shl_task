import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# === CONFIG ===
CSV_PATH = "./final_data_cleaned.csv"         # Your original SHL CSV
INDEX_FILE = "./shl_faiss3.index"        # FAISS index file to be created
MAPPING_FILE = "./shl_index_mapping3.pkl" # Mapping file to be saved

# === LOAD DATA ===
df = pd.read_csv(CSV_PATH)

# === TEXT REPRESENTATION FOR EMBEDDING ===
def create_text_representation(row):
    return (
        f"{row['Test Name']} | "
        f"{row['Test Type']} | "
        f"Remote: {row['Remote Testing']} | "
        f"Adaptive: {row['Adaptive/IRT']} | "
        f"Duration: {row['Duration (min)']} minutes | "
        f"{row['Test Link']}"
    )

df["text"] = df.apply(create_text_representation, axis=1)
documents = df["text"].tolist()

# === EMBEDDING MODEL ===
model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
embeddings = model.encode(documents, convert_to_tensor=False)

# === BUILD FAISS INDEX ===
dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# === SAVE FAISS INDEX & MAPPING ===
faiss.write_index(index, INDEX_FILE)
with open(MAPPING_FILE, "wb") as f:
    pickle.dump(df.to_dict(orient="records"), f)

print("Clean FAISS index and mapping saved.")
