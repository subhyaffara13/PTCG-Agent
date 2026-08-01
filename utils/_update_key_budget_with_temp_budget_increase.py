
def _update_key_budget_with_temp_budget_increase(
    valid_token: UserAPIKeyAuth,
) -> UserAPIKeyAuth:
    if valid_token.max_budget is None:
        return valid_token
    temp_budget_increase = _get_temp_budget_increase(valid_token) or 0.0
    valid_token.max_budget = valid_token.max_budget + temp_budget_increase
    return valid_token

