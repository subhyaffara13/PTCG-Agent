
def new_budget_request(data: NewCustomerRequest) -> Optional[BudgetNewRequest]:
    """
    Return a new budget object if new budget params are passed.
    """
    budget_params = BudgetNewRequest.model_fields.keys()
    budget_kv_pairs = {}

    # Get the actual values from the data object using getattr
    for field_name in budget_params:
        if field_name == "budget_id":
            continue
        value = getattr(data, field_name, None)
        if value is not None:
            budget_kv_pairs[field_name] = value

    if budget_kv_pairs:
        budget_request = BudgetNewRequest(**budget_kv_pairs)
        if (
            budget_request.budget_reset_at is None
            and budget_request.budget_duration is not None
        ):
            budget_request.budget_reset_at = datetime.utcnow() + timedelta(
                seconds=duration_in_seconds(duration=budget_request.budget_duration)
            )
        return budget_request
    return None

