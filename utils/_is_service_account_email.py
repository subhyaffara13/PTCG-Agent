
def _is_service_account_email(email):
    """Checks if the provided string is a service account email.

    This is a check that ensures the candidate string is non-empty
    and matches a standard email format.

    Args:
        email (str): The candidate string to check.

    Returns:
        bool: True if the string is non-empty and matches email format, False otherwise.
    """
    if not email:
        return False
    return bool(_SERVICE_ACCOUNT_EMAIL_PATTERN.match(email))

