
def _leaderboard_from_pairs(
    pair_scores: Iterable[dict[str, float]],
    models: list[str],
) -> list[tuple[str, float]]:
    """Score each model = sum of its pair-totals. Returns sorted descending."""
    cum: dict[str, float] = defaultdict(float)
    seen: dict[str, int] = defaultdict(int)
    for totals in pair_scores:
        for m, s in totals.items():
            cum[m] += s
            seen[m] += 1
    scored = [
        (m, cum.get(m, 0.0) / max(seen.get(m, 1), 1))
        for m in models
    ]
    scored.sort(key=lambda x: -x[1])
    return scored

