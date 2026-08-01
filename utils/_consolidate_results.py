
def _consolidate_results(results):
    for prefix, key in [("deck_test", "deck_test"), ("variance_baseline", "variance_baseline")]:
        workers = [res for k, res in results.items() if k.startswith(prefix)]
        if workers:
            win_counts = Counter(w.get("winner") for w in workers)
            results[key] = {"label": key, "winner": win_counts.most_common(1)[0][0],
                            "turns_taken": int(sum(w.get("turns_taken", 0) for w in workers) / len(workers)),
                            "prizes_taken_a": int(sum(w.get("prizes_taken_a", 0) for w in workers) / len(workers)),
                            "prizes_taken_b": int(sum(w.get("prizes_taken_b", 0) for w in workers) / len(workers)),
                            "time_elapsed": workers[0].get("time_elapsed", 0.0),
                            "timeout": any(w.get("timeout") for w in workers),
                            "log_files": workers[0].get("log_files", {})}

