import random

def generate_presets(
    *,
    seed: int,
    num_presets: int,
    num_hands: int,
    cards_per_hand: int,
    deck_size: int,
) -> Iterable[dict[str, object]]:
    rng = random.Random(seed)
    for preset_index in range(num_presets):
        hands = generate_hands(
            rng,
            num_hands=num_hands,
            cards_per_hand=cards_per_hand,
            deck_size=deck_size,
        )
        yield {
            "presetHands": hands,
            "seed": seed,
            "presetIndex": preset_index,
            "numHands": num_hands,
            "cardsPerHand": cards_per_hand,
            "deckSize": deck_size,
        }

