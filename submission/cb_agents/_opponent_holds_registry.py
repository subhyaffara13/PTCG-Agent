_registry = None

def _get_registry():
    global _registry
    if _registry is None:
        from cb_agents.card_registry import CardRegistry
        _registry = CardRegistry()
    return _registry
