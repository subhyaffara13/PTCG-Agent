import json
import os
import re

def _save_confusion_results(label: str, metrics: dict, wrong: list, rows: list) -> dict:
    """Save confusion matrix results to a JSON file and return the result dict."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    # Build a short, filesystem-safe filename from the label.
    # Full label is preserved inside the JSON; filename just needs to be
    # unique and recognisable.  Format: {topic}_{method_abbrev}.json
    parts = label.split("\u2014")
    topic = parts[0].strip().lower().replace("block ", "").replace(" ", "_")
    method_full = parts[1].strip() if len(parts) > 1 else ""
    method_name = re.sub(r"\s*\(.*?\)", "", method_full).strip().lower()
    qualifier_match = re.search(r"\(([^)]+)\)", method_full)
    qualifier = qualifier_match.group(1) if qualifier_match else ""
    qualifier = re.sub(r"\.[a-z]+$", "", qualifier)  # drop .yaml etc.
    if method_name == "contentfilter":
        safe_label = f"{topic}_cf"
    elif qualifier:
        safe_label = f"{topic}_{method_name}_{qualifier}"
    else:
        safe_label = f"{topic}_{method_name}"
    safe_label = safe_label.replace(" ", "_")
    safe_label = re.sub(r"[^a-z0-9_.\-]", "", safe_label)
    safe_label = re.sub(r"_+", "_", safe_label).strip("_")
    result = {
        "label": label,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total": metrics["total"],
        "tp": metrics["tp"],
        "tn": metrics["tn"],
        "fp": metrics["fp"],
        "fn": metrics["fn"],
        "precision": round(metrics["precision"], 4),
        "recall": round(metrics["recall"], 4),
        "f1": round(metrics["f1"], 4),
        "accuracy": round(metrics["accuracy"], 4),
        "latency_p50_ms": round(metrics["p50"], 3),
        "latency_p95_ms": round(metrics["p95"], 3),
        "latency_avg_ms": round(metrics["avg_lat"], 3),
        "wrong": wrong,
        "rows": rows,
    }
    result_path = os.path.join(RESULTS_DIR, f"{safe_label}.json")
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)
    return result

