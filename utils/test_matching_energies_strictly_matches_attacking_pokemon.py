
def test_matching_energies_strictly_matches_attacking_pokemon(sample_pool_and_details):
    card_pool, card_details = sample_pool_and_details
    gen = DeckGenerator(card_pool, card_details, {})

    # Deck with only Fire Pokemon
    deck = [card_details["1"], card_details["2"]]
    matching = gen._matching_energies(deck, card_pool)
    matching_names = [c["card_name"] for c in matching]

    assert "Basic {R} Energy" in matching_names
    assert "Basic {W} Energy" not in matching_names

