import json

# === Path to JSON File ===
DATA = "./evaluation_data.json"

# === Normalize URL for accurate comparison ===
def normalize(url):
    return url.strip().lower().rstrip("/")

# === Recall@K ===
def recall_at_k(ground_truth, predictions, k):
    top_k = predictions[:k]
    hits = sum(1 for item in ground_truth if normalize(item) in [normalize(p) for p in top_k])
    return hits / len(ground_truth) if ground_truth else 0

# === MAP@K ===
def average_precision_at_k(ground_truth, predictions, k):
    score = 0.0
    hits = 0
    normalized_gt = [normalize(g) for g in ground_truth]
    for i, p in enumerate(predictions[:k]):
        if normalize(p) in normalized_gt:
            hits += 1
            score += hits / (i + 1)
    return score / min(len(ground_truth), k) if ground_truth else 0

# === Evaluation Function ===
def evaluate(json_path, k_values=[3, 5]):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = {f"Recall@{k}": [] for k in k_values}
    results.update({f"MAP@{k}": [] for k in k_values})

    for item in data:
        ground = item["ground_truth"]
        preds = item["model_output"]

        for k in k_values:
            results[f"Recall@{k}"].append(recall_at_k(ground, preds, k))
            results[f"MAP@{k}"].append(average_precision_at_k(ground, preds, k))

    # === Compute Average Scores ===
    for key in results:
        avg = sum(results[key]) / len(results[key]) if results[key] else 0
        print(f"{key}: {avg:.4f}")

# === Run the Evaluation ===
if __name__ == "__main__":
    evaluate(DATA, k_values=[1,10])
