
def _pair_score_per_model(
    rows: list[dict],
) -> dict[tuple, dict[str, float]]:
    """Aggregate raw rows into ``{pair_id: {model: total_score_in_pair}}``."""
    totals: dict[tuple, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    counts: dict[tuple, int] = defaultdict(int)
    for r in rows:
        pid = _pair_id(r)
        totals[pid][r["model_p0"]] += float(r["score_p0"])
        totals[pid][r["model_p1"]] += float(r["score_p1"])
        counts[pid] += 1
    # Only keep complete pairs (both seat-flipped games present).
    return {pid: ts for pid, ts in totals.items() if counts[pid] == 2}

