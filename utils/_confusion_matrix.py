
def _confusion_matrix(checker, cases: List[dict], label: str):
    """Run all cases, print confusion matrix, save results JSON."""
    tp = fp = tn = fn = 0
    wrong = []
    rows = []
    latencies = []

    for case in cases:
        expected = case["expected"]
        t0 = time.perf_counter()
        result = _run(checker, case["sentence"])
        latency_ms = (time.perf_counter() - t0) * 1000
        latencies.append(latency_ms)
        actual = result["decision"]
        score = result["score"]
        matched_topic = result.get("matched_topic")
        correct = expected == actual

        rows.append(
            {
                "sentence": case["sentence"],
                "expected": expected,
                "actual": actual,
                "correct": correct,
                "test": case["test"],
                "score": score,
                "matched_topic": matched_topic,
                "latency_ms": round(latency_ms, 3),
            }
        )

        if expected == "BLOCK" and actual == "BLOCK":
            tp += 1
        elif expected == "ALLOW" and actual == "ALLOW":
            tn += 1
        elif expected == "BLOCK" and actual == "ALLOW":
            fn += 1
            wrong.append(
                f"  FN (score={score:.3f}): {case['sentence']!r:60s} — {case['test']}"
            )
        elif expected == "ALLOW" and actual == "BLOCK":
            fp += 1
            wrong.append(
                f"  FP (score={score:.3f}): {case['sentence']!r:60s} — {case['test']}"
            )

    total = tp + tn + fp + fn
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (
        2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    )
    accuracy = (tp + tn) / total if total > 0 else 0

    # Latency stats
    sorted_lat = sorted(latencies)
    p50 = sorted_lat[len(sorted_lat) // 2] if sorted_lat else 0
    p95 = sorted_lat[int(len(sorted_lat) * 0.95)] if sorted_lat else 0
    avg_lat = sum(latencies) / len(latencies) if latencies else 0

    metrics = {
        "total": total,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
        "p50": p50,
        "p95": p95,
        "avg_lat": avg_lat,
    }
    _print_confusion_report(label, metrics, wrong)
    result = _save_confusion_results(label, metrics, wrong, rows)
    return result

