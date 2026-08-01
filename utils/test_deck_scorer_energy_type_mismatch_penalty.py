
def test_deck_scorer_energy_type_mismatch_penalty():
    # Deck with Pokemon needing Grass energy but only Fire/Lightning energy in deck
    mismatched_deck = [
        CardState("117", "cornerstone mask ogerpon ex", "Pokemon", "Basic", "", 2, 100, "{g}", set()),
        CardState("4", "basic {l} energy", "Energy", "", "", 0, 0, "{l}", set()),
        CardState("2", "basic {r} energy", "Energy", "", "", 0, 0, "{r}", set())
    ]
    ct = {"basic": 25, "sup": 25, "item": 10, "eng": 10, "s1": 0, "s2": 0, "attackers": [mismatched_deck[0]]}
    
    score_mismatched = consistency_score(mismatched_deck, ct)
    
    # Matching deck
    matching_deck = [
        CardState("37", "iron thorns ex", "Pokemon", "Basic", "", 2, 100, "{l}", set()),
        CardState("4", "basic {l} energy", "Energy", "", "", 0, 0, "{l}", set()),
        CardState("2", "basic {r} energy", "Energy", "", "", 0, 0, "{r}", set())
    ]
    ct_match = {"basic": 25, "sup": 25, "item": 10, "eng": 10, "s1": 0, "s2": 0, "attackers": [matching_deck[0]]}
    score_matching = consistency_score(matching_deck, ct_match)
    
    assert score_matching > score_mismatched

