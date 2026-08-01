
def _phase_instruction(
    phase: str,
    from_sq: str | None,
    to_sq: str | None,
) -> str:
    """Per-phase instruction text. Names the in-progress squares when known.

    The TO/SHOOT phases are the high-stakes ones: the engine has already
    cleared the queen's source cell, so the board no longer reveals which
    queen the player picked up. Without telling the model, it has to infer
    the source from the move-history list -- which it usually gets wrong,
    burning retries. We name ``from_sq`` / ``to_sq`` explicitly here.
    """
    if phase == "to":
        if from_sq is not None:
            return (
                f"You picked up the queen previously at {from_sq} -- that "
                f"square is now empty on the board. Choose where to move "
                f"it: any empty square reachable from {from_sq} by a "
                "queen-move (any number of empty squares in a straight or "
                "diagonal line; the path may not cross another queen or a "
                "blocked square)."
            )
        return (
            "You picked up one of your queens earlier this turn -- its "
            "previous square is now empty on the board. Choose where to "
            "move it: queens move any number of empty squares in a "
            "straight or diagonal line and cannot pass through other "
            "pieces or blocked squares."
        )
    if phase == "shoot":
        if from_sq is not None and to_sq is not None:
            return (
                f"Your queen moved from {from_sq} to {to_sq} this turn "
                f"and is now sitting at {to_sq}. Place a barrier on any "
                f"empty square reachable from {to_sq} by a queen-move "
                "(any number of empty squares in a straight or diagonal "
                f"line). This INCLUDES {from_sq}, the square the queen "
                "just vacated -- it is empty again and reachable, so it "
                "is a legal barrier target. The chosen square is then "
                "permanently blocked for the rest of the game: no piece "
                "may enter or cross it."
            )
        return (
            "Place a barrier from the queen you just moved. The barrier "
            "travels any number of empty squares from that queen's new "
            "square in a straight or diagonal line; the square it lands "
            "on is permanently blocked for the rest of the game. The "
            "square the queen just vacated this turn is empty again and "
            "is a legal barrier target."
        )
    # FROM phase
    return (
        "Choose which of your queens to move. You may only pick a queen "
        "that has at least one empty neighbouring square -- a queen with "
        "no empty neighbour cannot move and is not a legal selection."
    )

