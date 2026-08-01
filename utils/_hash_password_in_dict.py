
def _hash_password_in_dict(data: dict) -> None:
    """Hash password field in-place if present."""
    if "password" in data and data["password"] is not None:
        data["password"] = hash_password(data["password"])

