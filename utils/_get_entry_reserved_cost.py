
def _get_entry_reserved_cost(entry: dict, default_reserved_cost: float) -> float:
    try:
        return float(entry.get("reserved_cost", default_reserved_cost) or 0.0)
    except (TypeError, ValueError):
        return default_reserved_cost

