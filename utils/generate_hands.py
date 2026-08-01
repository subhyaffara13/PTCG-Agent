
def generate_hands(
    rng: random.Random,
    *,
    num_hands: int,
    cards_per_hand: int,
    deck_size: int,
) -> list[list[int]]:
    if not 0 < cards_per_hand <= deck_size:
        raise ValueError(
            f"cards_per_hand must be in [1, deck_size]; got cards_per_hand={cards_per_hand}, deck_size={deck_size}."
        )
    return [rng.sample(range(deck_size), cards_per_hand) for _ in range(num_hands)]

