
def _build_member_budget_patch(data: TeamMemberUpdateRequest) -> Dict[str, Any]:
    """Map the budget fields the request actually set (merge-patch: a sent
    value updates, an explicit null clears, an absent field is left untouched)
    to their budget-table columns."""
    provided = data.model_dump(exclude_unset=True)
    return {
        column: provided[request_field]
        for request_field, column in _MEMBER_BUDGET_PATCH_FIELDS.items()
        if request_field in provided
    }

