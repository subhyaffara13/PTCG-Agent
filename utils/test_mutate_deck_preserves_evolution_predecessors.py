
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

