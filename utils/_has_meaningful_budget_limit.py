
def _has_meaningful_budget_limit(budget_values: Dict[str, Any]) -> bool:
    """A budget is meaningful if at least one limit is actually set; an empty
    list (no model restriction) and None both count as unset."""
    return any(
        _is_set_budget_value(budget_values.get(field))
        for field in _TEAM_MEMBER_BUDGET_LIMIT_FIELDS
    )

