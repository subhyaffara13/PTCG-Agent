
def normalize_email(email: Optional[str]) -> Optional[str]:
    """
    Normalize email address to lowercase for consistent storage and comparison.

    Email addresses should be treated as case-insensitive for SSO purposes,
    even though RFC 5321 technically allows case-sensitive local parts.
    This prevents issues where SSO providers return emails with different casing
    than what's stored in the database.

    Args:
        email: Email address to normalize, can be None

    Returns:
        Lowercased email address, or None if input is None
    """
    if email is None:
        return None
    return email.lower() if isinstance(email, str) else email

