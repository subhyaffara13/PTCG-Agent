
def check_if_token_is_service_account(valid_token: UserAPIKeyAuth) -> bool:
    """
    Checks if the token is a service account

    Returns:
        bool: True if token is a service account

    """
    if valid_token.metadata:
        if "service_account_id" in valid_token.metadata:
            return True
    return False

