"""
tests/test_deck_generator_fixes.py

Unit tests for deck_generator fixes: evolution dependencies, basic pokemon counts,
replacement card verification, and strict matching energies.
"""
import pytest
from factory.deck_generator import DeckGenerator

@pytest.fixture
def sample_pool_and_details():
    card_pool = [
        {"card_id": "1", "card_name": "Charmander", "card_type": "Pokemon", "archetype": "aggro"},
        {"card_id": "2", "card_name": "Charmeleon", "card_type": "Pokemon", "archetype": "aggro"},
        {"card_id": "3", "card_name": "Charizard", "card_type": "Pokemon", "archetype": "aggro"},
        {"card_id": "4", "card_name": "Basic {R} Energy", "card_type": "Energy", "archetype": "utility"},
        {"card_id": "5", "card_name": "Basic {W} Energy", "card_type": "Energy", "archetype": "utility"},
        {"card_id": "6", "card_name": "Nest Ball", "card_type": "Trainer", "archetype": "utility"},
        {"card_id": "7", "card_name": "Squirtle", "card_type": "Pokemon", "archetype": "aggro"},
        {"card_id": "8", "card_name": "Wartortle", "card_type": "Pokemon", "archetype": "aggro"},
    ]
    card_details = {
        "1": {"card_id": "1", "card_name": "Charmander", "card_type": "Pokemon", "stage": "Basic", "element_type": "{R}"},
        "2": {"card_id": "2", "card_name": "Charmeleon", "card_type": "Pokemon", "stage": "Stage 1", "previous_stage": "Charmander", "element_type": "{R}"},
        "3": {"card_id": "3", "card_name": "Charizard", "card_type": "Pokemon", "stage": "Stage 2", "previous_stage": "Charmeleon", "element_type": "{R}"},
        "4": {"card_id": "4", "card_name": "Basic {R} Energy", "card_type": "Energy", "stage": "Basic", "element_type": "{R}"},
        "5": {"card_id": "5", "card_name": "Basic {W} Energy", "card_type": "Energy", "stage": "Basic", "element_type": "{W}"},
        "6": {"card_id": "6", "card_name": "Nest Ball", "card_type": "Trainer", "stage": "Basic", "element_type": ""},
        "7": {"card_id": "7", "card_name": "Squirtle", "card_type": "Pokemon", "stage": "Basic", "element_type": "{W}"},
        "8": {"card_id": "8", "card_name": "Wartortle", "card_type": "Pokemon", "stage": "Stage 1", "previous_stage": "Squirtle", "element_type": "{W}"},
    }
    return card_pool, card_details

def test_matching_energies_strictly_matches_attacking_pokemon(sample_pool_and_details):
    card_pool, card_details = sample_pool_and_details
    gen = DeckGenerator(card_pool, card_details, {})

    # Deck with only Fire Pokemon
    deck = [card_details["1"], card_details["2"]]
    matching = gen._matching_energies(deck, card_pool)
    matching_names = [c["card_name"] for c in matching]

    assert "Basic {R} Energy" in matching_names
    assert "Basic {W} Energy" not in matching_names

def test_mutate_deck_preserves_evolution_predecessors(sample_pool_and_details):
    card_pool, card_details = sample_pool_and_details
    gen = DeckGenerator(card_pool, card_details, {})

    # Build a 60 card deck: 12 Charmander, 4 Charmeleon, 4 Charizard, 20 Nest Ball, 20 Basic {R} Energy
    deck = [dict(card_pool[0])]*12 + [dict(card_pool[1])]*4 + [dict(card_pool[2])]*4 + [dict(card_pool[5])]*20 + [dict(card_pool[3])]*20
    legal_cards = card_pool
    basic_pokemon = [card_pool[0]]

    mutated = gen.mutate_deck(deck, num_swaps=5, legal_cards=legal_cards, basic_pokemon=basic_pokemon)
    assert len(mutated) == 60

    # Ensure no Stage 1 or Stage 2 pokemon is left without its predecessor in mutated deck
    mutated_names = {c.get("card_name", "").lower() for c in mutated if c.get("card_type") == "Pokemon"}
    for c in mutated:
        if c.get("card_type") == "Pokemon":
            det = card_details.get(str(c.get("card_id")), {})
            stg = det.get("stage")
            if stg in ("Stage 1", "Stage 2"):
                prev = det.get("previous_stage")
                assert prev is not None
                assert prev.lower() in mutated_names

def test_mutate_deck_maintains_at_least_12_basics(sample_pool_and_details):
    card_pool, card_details = sample_pool_and_details
    gen = DeckGenerator(card_pool, card_details, {})

    deck = [dict(card_pool[0])]*12 + [dict(card_pool[1])]*4 + [dict(card_pool[2])]*4 + [dict(card_pool[5])]*20 + [dict(card_pool[3])]*20
    legal_cards = card_pool
    basic_pokemon = [card_pool[0]]

    mutated = gen.mutate_deck(deck, num_swaps=10, legal_cards=legal_cards, basic_pokemon=basic_pokemon)
    basics_count = sum(
        1 for c in mutated
        if c.get("card_type") == "Pokemon" and card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic"
    )
    assert basics_count >= 12
