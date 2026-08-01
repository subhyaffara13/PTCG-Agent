
def get_energy_preference(card_id: str) -> str | None:
    """Return the preferred energy card ID for a given Pokemon card ID."""
    global _DYNAMIC_PREFERENCE_MAP
    if _DYNAMIC_PREFERENCE_MAP is None:
        _initialize_preference_map()
    return _DYNAMIC_PREFERENCE_MAP.get(str(card_id))


def get_energy_preference(card_id: str) -> str | None:
    """Return the preferred energy card ID for a given Pokemon card ID."""
    if _DYNAMIC_PREFERENCE_MAP is None:
        _initialize_preference_map()
    return _DYNAMIC_PREFERENCE_MAP.get(str(card_id))


def get_energy_preference(card_id: str) -> str | None:
    """Return the preferred energy card ID for a given Pokemon card ID."""
    if _DYNAMIC_PREFERENCE_MAP is None:
        _initialize_preference_map()
    return _DYNAMIC_PREFERENCE_MAP.get(str(card_id))

