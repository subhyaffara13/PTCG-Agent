
def test_value_network_clipping_allows_negative_heuristics():
    nn = NeuralValueNetwork()
    # Mock game state with dangerous low deck where Lillie's Determination gets severe penalty
    game_state = {"my_deck_count": 2, "my_bench": [1], "my_hand": [1227]}
    val = nn.evaluate(game_state, action="play_trainer:Lillie's Determination")
    
    # The value should be below -1.0 due to -10.0 penalty, not clamped to -1.0
    assert val < -1.0

