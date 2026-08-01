
def _get_preset_hands(configuration: dict[str, Any]) -> list[list[int]]:
    preset_hands = configuration.get("presetHands")
    if not preset_hands:
        return []
    if configuration.get("useOpenings"):
        raise ValueError("Cannot set both useOpenings and presetHands.")
    if (
        configuration.get("loadPresetHands")
        and "presetHands" in configuration
        and not configuration.get("_presetHandsLoaded")
    ):
        raise ValueError("Cannot set both loadPresetHands and presetHands.")
    if configuration.get("initialActions"):
        raise ValueError("Cannot set both initialActions and presetHands.")
    game_name = configuration.get("openSpielGameName")
    if game_name != "repeated_poker":
        raise ValueError(f"presetHands only supported for repeated_poker, not {game_name}.")
    validated: list[list[int]] = []
    for hand_index, hand in enumerate(preset_hands):
        if not isinstance(hand, list):
            raise ValueError(f"presetHands[{hand_index}] must be a list of integers.")
        if any(not isinstance(action, int) for action in hand):
            raise ValueError(f"presetHands[{hand_index}] must contain only integers.")
        validated.append(list(hand))
    return validated

