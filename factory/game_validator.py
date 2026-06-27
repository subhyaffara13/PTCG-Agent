def validate_mcts_step(game_state, action, damage):
    if "my_hand" in game_state and len(game_state["my_hand"]) == 0:
        raise RuntimeError("my_hand is completely empty, preventing energy attachment")
    if action == "ATTACK_KO" and damage == 0:
        raise RuntimeError("action is ATTACK_KO but damage is 0")
    if game_state.get("select_prize") and action == "pass":
        raise RuntimeError("state requires prize selection but action defaults to pass")
