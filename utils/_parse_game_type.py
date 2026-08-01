
def _parse_game_type(game_type: str) -> dict[str, bool]:
    """Parse 'Base+MLP' style expansion suffix into a flag dict."""
    suffix = game_type.split("+", 1)[1] if "+" in game_type else ""
    return {
        "mosquito": "M" in suffix,
        "ladybug": "L" in suffix,
        "pillbug": "P" in suffix,
    }

