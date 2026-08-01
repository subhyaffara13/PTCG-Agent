
def test_genetic_mutation_copy_limits():
    from scratch.deck_genetics import mutate_deck
    from collections import Counter
    card_a = {"card_id": 1, "card_type": "Pokemon", "card_name": "Pikachu"}
    card_b = {"card_id": 2, "card_type": "Trainer", "card_name": "Nest Ball"}
    card_energy = {"card_id": 3, "card_type": "Energy", "card_name": "Basic {W} Energy"}
    
    deck = [card_a]*4 + [card_b]*4 + [card_energy]*52
    pool_cards = [card_a, card_b, card_energy]
    details = {
        "1": {"card_id": 1, "card_name": "Pikachu", "card_type": "Pokemon"},
        "2": {"card_id": 2, "card_name": "Nest Ball", "card_type": "Trainer"},
        "3": {"card_id": 3, "card_name": "Basic {W} Energy", "card_type": "Energy"}
    }
    
    for _ in range(50):
        deck = mutate_deck(
            deck=deck,
            pokemon_pool=[card_a],
            basics=[card_a],
            energy_pool=[card_energy],
            trainer_pool={"Nest Ball": 4},
            pool_cards=pool_cards,
            details=details,
            mutation_rate=1.0
        )
        counts = Counter(c["card_id"] for c in deck)
        for cid, count in counts.items():
            card = next(x for x in pool_cards if x["card_id"] == cid)
            is_basic_energy = "ENERGY" in str(card.get("card_type")).upper() and "BASIC" in str(card.get("card_name", "")).upper()
            if not is_basic_energy:
                assert count <= 4, f"Card {card['card_name']} exceeded 4 copies: count is {count}"

