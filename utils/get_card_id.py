
def get_card_id(c):
    if hasattr(c, "id"): return getattr(c, "id")
    if isinstance(c, dict): return c.get("id") or c.get("cardId") or c.get("name")
    return None

