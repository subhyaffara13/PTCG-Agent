
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

