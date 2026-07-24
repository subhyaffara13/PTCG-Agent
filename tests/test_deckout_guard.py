import pytest
from cb_agents.heuristic_pipeline_check import mask_illegal
from cb_agents.turn_planner_sort import sort_actions_heuristically
from factory.deck_scorer_consistency import consistency_score
from factory.deck_scorer_state import CardState

def test_mask_illegal_prunes_draw_supporters_when_deck_low():
    # Test deck count = 3 (similar to Step 239 in episode 87899958)
    game_state_low_deck = {
        "my_deck_count": 3,
        "my_bench": [1],
        "my_hand": [117, 1081, 1227]
    }
    legal_actions = [
        "play_trainer:Lillie's Determination",
        "play_trainer:Enhanced Hammer",
        "attack:Knockout",
        "pass"
    ]
    
    filtered = mask_illegal(legal_actions, game_state_low_deck)
    
    # Lillie's Determination should be hard-pruned from candidate list
    assert "play_trainer:Lillie's Determination" not in filtered
    assert "play_trainer:Enhanced Hammer" in filtered
    assert "attack:Knockout" in filtered

def test_turn_planner_sort_penalizes_low_deck_draw_supporters():
    game_state = {
        "my_deck_count": 4,
        "opponent_deck_count": 20,
        "my_bench": [1],
        "my_hand": [1227]
    }
    candidates = [
        "play_trainer:Lillie's Determination",
        "attack:Attack1",
        "pass"
    ]
    
    sorted_actions = sort_actions_heuristically(candidates, "aggro_push", game_state)
    
    # Lillie's Determination should be ranked AFTER attack
    assert sorted_actions.index("play_trainer:Lillie's Determination") > sorted_actions.index("attack:Attack1")

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
