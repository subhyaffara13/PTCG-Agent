
def update_valid_token_with_end_user_params(
    valid_token: UserAPIKeyAuth, end_user_params: dict
) -> UserAPIKeyAuth:
    valid_token.end_user_id = end_user_params.get("end_user_id")
    # Only overwrite token fields when the DB-derived value is not None.
    # This prevents DB lookups (where the budget table has no value set)
    # from silently clearing values that a custom auth function may have
    # already set on the token.
    if end_user_params.get("end_user_tpm_limit") is not None:
        valid_token.end_user_tpm_limit = end_user_params["end_user_tpm_limit"]
    if end_user_params.get("end_user_rpm_limit") is not None:
        valid_token.end_user_rpm_limit = end_user_params["end_user_rpm_limit"]
    if end_user_params.get("allowed_model_region") is not None:
        valid_token.allowed_model_region = end_user_params["allowed_model_region"]
    if end_user_params.get("end_user_model_max_budget") is not None:
        valid_token.end_user_model_max_budget = end_user_params[
            "end_user_model_max_budget"
        ]
    return valid_token

