
def _validate_reset_spend_value(
    reset_to: Any, key_in_db: LiteLLM_VerificationToken
) -> float:
    if not isinstance(reset_to, (int, float)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "reset_to must be a float"},
        )

    reset_to = float(reset_to)

    if reset_to < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "reset_to must be >= 0"},
        )

    current_spend = key_in_db.spend or 0.0
    if reset_to > current_spend:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": f"reset_to ({reset_to}) must be <= current spend ({current_spend})"
            },
        )

    max_budget = key_in_db.max_budget
    if key_in_db.litellm_budget_table is not None:
        budget_max_budget = getattr(key_in_db.litellm_budget_table, "max_budget", None)
        if budget_max_budget is not None:
            if max_budget is None or budget_max_budget < max_budget:
                max_budget = budget_max_budget

    if max_budget is not None and reset_to > max_budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": f"reset_to ({reset_to}) must be <= budget ({max_budget})"},
        )

    return reset_to

