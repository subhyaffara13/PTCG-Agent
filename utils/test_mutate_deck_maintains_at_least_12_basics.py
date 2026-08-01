
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

