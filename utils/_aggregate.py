
def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Build the per-variant / per-model statistics shown in summary.md."""
    # Per (variant, model) accumulators.
    games_played: dict[tuple[str, str], int] = defaultdict(int)
    game_wins: dict[tuple[str, str], float] = defaultdict(float)
    score_sum: dict[tuple[str, str], float] = defaultdict(float)
    score_n: dict[tuple[str, str], int] = defaultdict(int)
    crash_count: dict[tuple[str, str], int] = defaultdict(int)

    # Per (variant, pair_key) for pair-win aggregation. pair_key is the
    # unordered pair tuple + seed, so we can sum both seat-flipped games.
    # pair_totals[(variant, frozenset({A,B}), seed)][model] = total_score
    pair_totals: dict[tuple, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    pair_games: dict[tuple, int] = defaultdict(int)

    for row in rows:
        v = row["variant"]
        m0, m1 = row["model_p0"], row["model_p1"]
        s0, s1 = float(row["score_p0"]), float(row["score_p1"])
        winner = int(row["winner"])
        seed = int(row["seed"])

        for model, score, crashed, won_flag in (
            (m0, s0, row["crash_p0"], 1.0 if winner == 1 else 0.5 if winner == 0 else 0.0),
            (m1, s1, row["crash_p1"], 1.0 if winner == -1 else 0.5 if winner == 0 else 0.0),
        ):
            games_played[(v, model)] += 1
            game_wins[(v, model)] += won_flag
            score_sum[(v, model)] += score
            score_n[(v, model)] += 1
            if str(crashed).lower() == "true":
                crash_count[(v, model)] += 1

        if row["pair_role"] in ("AB", "BA") and m0 != m1:
            pair_key = (v, frozenset((m0, m1)), seed)
            pair_totals[pair_key][m0] += s0
            pair_totals[pair_key][m1] += s1
            pair_games[pair_key] += 1

    # Per (variant, model) pair-wins. A pair counts when both seat-flipped
    # games for that pair_key are complete (pair_games[k] == 2).
    pair_wins: dict[tuple[str, str], float] = defaultdict(float)
    pair_counts: dict[tuple[str, str], int] = defaultdict(int)
    for pair_key, totals in pair_totals.items():
        if pair_games[pair_key] != 2:
            continue
        v = pair_key[0]
        models_in_pair = list(totals.keys())
        if len(models_in_pair) != 2:
            continue
        a, b = models_in_pair
        ta, tb = totals[a], totals[b]
        for m in (a, b):
            pair_counts[(v, m)] += 1
        if ta > tb:
            pair_wins[(v, a)] += 1.0
        elif tb > ta:
            pair_wins[(v, b)] += 1.0
        else:
            pair_wins[(v, a)] += 0.5
            pair_wins[(v, b)] += 0.5

    return {
        "games_played": games_played,
        "game_wins": game_wins,
        "score_sum": score_sum,
        "score_n": score_n,
        "crash_count": crash_count,
        "pair_wins": pair_wins,
        "pair_counts": pair_counts,
    }

