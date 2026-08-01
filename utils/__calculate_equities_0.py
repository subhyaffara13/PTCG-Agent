
def __calculate_equities_0(
        hole_cards: tuple[list[Card], ...],
        board_cards: list[Card],
        hole_dealing_count: int,
        board_dealing_count: int,
        deck_cards: list[Card],
        hand_types: tuple[type[Hand], ...],
) -> list[float]:
    hole_cards = tuple(map(list.copy, hole_cards))
    board_cards = board_cards.copy()
    sample_count = (
        (hole_dealing_count * len(hole_cards))
        - sum(map(len, hole_cards))
        + board_dealing_count
        - len(board_cards)
    )
    sampled_cards = sample(deck_cards, k=sample_count)
    begin = 0

    for i in range(len(hole_cards)):
        end = begin + hole_dealing_count - len(hole_cards[i])

        hole_cards[i].extend(sampled_cards[begin:end])

        assert len(hole_cards[i]) == hole_dealing_count

        begin = end

    board_cards.extend(sampled_cards[begin:])

    assert len(board_cards) == board_dealing_count

    equities = [0.0] * len(hole_cards)

    for hand_type in hand_types:
        hands = list(
            map(
                partial(hand_type.from_game_or_none, board_cards=board_cards),
                hole_cards,
            ),
        )
        max_hand = max_or_none(hands)
        statuses = list(map(partial(eq, max_hand), hands))
        increment = 1 / (len(hand_types) * sum(statuses))

        for i, status in enumerate(statuses):
            if status:
                equities[i] += increment

    return equities

