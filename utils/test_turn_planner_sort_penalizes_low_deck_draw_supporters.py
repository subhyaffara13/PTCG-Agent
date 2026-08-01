
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

