
def _get_temp_budget_increase(valid_token: UserAPIKeyAuth):
    valid_token_metadata = valid_token.metadata
    if (
        "temp_budget_increase" in valid_token_metadata
        and "temp_budget_expiry" in valid_token_metadata
    ):
        expiry = datetime.fromisoformat(valid_token_metadata["temp_budget_expiry"])
        if expiry > datetime.now():
            return valid_token_metadata["temp_budget_increase"]
    return None

