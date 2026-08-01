
def _compute_trend_stats(data, trend_stats):
    turns = [entry.get("turn", 1) for entry in data]
    max_turn = max(turns) if turns else 1
    trend_stats["total_turns"] += max_turn
    if max_turn >= 100: trend_stats["timeouts"] += 1
    if max_turn <= 5: trend_stats["fast_losses"] += 1

