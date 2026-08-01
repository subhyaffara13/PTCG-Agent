
def battle_start(deck0: list[int], deck1: list[int]) -> tuple[dict, StartData]:
    """Start the battle.

    Args:
        deck0: List of card IDs included in the first player’s deck.
        deck1: List of card IDs included in the second player’s deck.

    Returns:
        tuple: A tuple containing:
            - dict: First observation.
            - StartData: Battle start data.
    """
    if len(deck0) != 60 or len(deck1) != 60:
        raise ValueError("The deck must contain 60 cards.")
    cards = deck0 + deck1
    arg = (ctypes.c_int * len(cards))(*cards)
    start_data = lib.BattleStart(arg)
    Battle.battle_ptr = start_data.battlePtr
    if Battle.battle_ptr == None or Battle.battle_ptr == 0:
        return (None, start_data)
    else:
        return (_get_battle_data(), start_data)

