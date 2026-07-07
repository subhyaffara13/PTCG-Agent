"""
agents/preference_maps.py
Contains static energy card preference mappings for optimal Pokemon attachments.
"""

ENERGY_PREFERENCE_MAP = {
    "957": "4", "87": "4", "734": "4", "733": "4", "950": "4",
    "979": "6", "226": "6", "855": "2"
}

def get_energy_preference(card_id: str) -> str | None:
    """Return the preferred energy card ID for a given Pokemon card ID."""
    return ENERGY_PREFERENCE_MAP.get(str(card_id))
