
def test_profile_orders_are_distinct():
    game_state = {"my_deck_count": 60, "my_bench": [1]}
    candidates = [
        "attack:Attack1",
        "bench:1",
        "attach_energy:4:1",
        "play_trainer:Lillie's Determination",
        "retreat:1",
        "pass"
    ]
    
    order_setup = sort_actions_heuristically(candidates, "setup", game_state)
    order_aggro = sort_actions_heuristically(candidates, "aggro_push", game_state)
    order_stall = sort_actions_heuristically(candidates, "stall", game_state)
    order_closing = sort_actions_heuristically(candidates, "closing", game_state)
    
    # Assert that distinct profiles produce distinct action rankings
    assert order_closing[0] == "attack:Attack1"
    assert order_stall[0] == "play_trainer:Lillie's Determination" or order_stall[-1] == "pass"
    assert order_setup != order_closing

