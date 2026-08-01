
def get_reserved_counter_keys(budget_reservation: Optional[dict]) -> set:
    if not budget_reservation:
        return set()
    entries = budget_reservation.get("entries") or []
    return {
        entry["counter_key"]
        for entry in entries
        if isinstance(entry, dict) and entry.get("counter_key") is not None
    }

