
def _valid_user_id(user_id: str) -> bool:
    """
    Validate that user_id is not an email or phone number.
    Returns: bool: True if valid (not email or phone), False otherwise
    """
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    phone_pattern = r"^\+?[\d\s\(\)-]{7,}$"

    if re.match(email_pattern, user_id):
        return False
    if re.match(phone_pattern, user_id):
        return False

    return True

