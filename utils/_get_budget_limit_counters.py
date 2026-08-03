from typing import Any, List, Optional

def _get_budget_limit_counters(
    entity_prefix: str,
    entity_type: str,
    entity_id: str,
    budget_limits: Optional[Sequence[Any]],
    fallback_spend: float,
) -> List[_BudgetCounter]:
    counters: List[_BudgetCounter] = []
    if not budget_limits:
        return counters

    for window in budget_limits:
        window_dict = _coerce_window(window)
        budget_duration = window_dict.get("budget_duration")
        max_budget = window_dict.get("max_budget")
        if not budget_duration or max_budget is None or max_budget <= 0:
            continue
        window_start = get_budget_window_start(window_dict)
        if window_start is None:
            verbose_proxy_logger.warning(
                "Skipping budget window with invalid duration for %s=%s: %s",
                entity_type,
                entity_id,
                budget_duration,
            )
            continue
        counters.append(
            _BudgetCounter(
                counter_key=f"{entity_prefix}:window:{budget_duration}",
                max_budget=float(max_budget),
                fallback_spend=0.0,
                entity_type=entity_type,
                entity_id=f"{entity_id}:{budget_duration}",
                spend_log_entity_id=entity_id,
                window_start=window_start,
            )
        )
    return counters

