
def get_card_identifier(card_id: Any) -> str:
    global _registry
    if _registry is None:
        _registry = CardRegistry()
    entry = _registry.get(card_id)
    if entry:
        return entry.card_name.lower().replace(" ", "-")
    return str(card_id).lower()


def get_card_identifier(card_id: Any) -> str:
    global _registry
    if _registry is None:
        _registry = CardRegistry()
    entry = _registry.get(card_id)
    if entry:
        return entry.card_name.lower().replace(" ", "-")
    return str(card_id).lower()

