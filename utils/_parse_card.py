
def _parse_card(token: str) -> str | None:
    if token == "XX" or not token:
        return None
    return token

