
def _compute_health_metrics(win_rate_history, diversity_history, mid):
    old_wr = sum(win_rate_history[:mid]) / max(1, mid)
    new_wr = sum(win_rate_history[mid:]) / max(1, len(win_rate_history) - mid)
    old_div = sum(diversity_history[:mid]) / max(1, mid)
    new_div = sum(diversity_history[mid:]) / max(1, len(diversity_history) - mid)
    return old_wr, new_wr, old_div, new_div

