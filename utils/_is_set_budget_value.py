
def _is_set_budget_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, list) and len(value) == 0:
        return False
    return True

