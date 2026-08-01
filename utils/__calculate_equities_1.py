
def __calculate_equities_1(
        hole_cards: list[tuple[list[Card], ...]],
        board_cards: list[Card],
        hole_dealing_count: int,
        board_dealing_count: int,
        deck_cards: list[list[Card]],
        hand_types: tuple[type[Hand], ...],
        index: int,
) -> list[float]:
    return __calculate_equities_0(
        hole_cards[index],
        board_cards,
        hole_dealing_count,
        board_dealing_count,
        deck_cards[index],
        hand_types,
    )

