
def _strip_password_from_response(response) -> None:
    """Strip password from API response (handles dicts, nested dicts, and Prisma models)."""
    if isinstance(response, dict):
        response.pop("password", None)
        if isinstance(response.get("data"), dict):
            response["data"].pop("password", None)
        elif hasattr(response.get("data"), "__dict__"):
            response["data"].__dict__.pop("password", None)

