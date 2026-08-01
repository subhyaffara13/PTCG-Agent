
def _get_attack_range(unit_type):
    """Return (min_range, max_range) for a unit type."""
    if unit_type in ("M", "S"):
        return (1, 2)
    if unit_type == "A":
        return (2, 3)
    return (1, 1)

