
def _get_enchant_dicts() -> list[tuple[Any, enchant.ProviderDesc]]:
    return enchant.Broker().list_dicts() if PYENCHANT_AVAILABLE else []

