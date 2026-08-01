
def _strip_password_from_users(users) -> None:
    """Strip password field from a list of user objects."""
    for user in users if isinstance(users, list) else [users]:
        if user and hasattr(user, "__dict__"):
            user.__dict__.pop("password", None)
        elif isinstance(user, dict):
            user.pop("password", None)

