
def _count_unrevealed_with_role(observation: Mapping[str, Any], role: str) -> int:
    """Count cells whose role equals ``role`` and that are still hidden.

    Only meaningful when the observation carries unmasked roles (i.e. the
    Cluemaster's view); guesser observations have ``"Unknown"`` for every
    hidden cell, so the count would always be 0.
    """
    roles = observation.get("roles", [])
    revealed = observation.get("revealed", [])
    return sum(
        1 for i in range(len(roles))
        if i < len(revealed) and not revealed[i] and roles[i] == role
    )

