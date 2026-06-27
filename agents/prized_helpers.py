from agents.card_types import CardType
from agents.card_registry import CardRegistry

_registry = CardRegistry()

def prized_pokemon_probs(prized_probabilities: dict, decklist: dict = None) -> list:
    probs = []
    try:
        for cid_str, prob in prized_probabilities.items():
            card = _registry.get(int(cid_str))
            if card and card.card_type == CardType.POKEMON:
                if decklist:
                    count = decklist.get(int(cid_str), decklist.get(cid_str, 0))
                    if count < 2:
                        continue
                probs.append(prob)
    except:
        probs = list(prized_probabilities.values())
    return probs
