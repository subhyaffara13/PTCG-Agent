
def parse_player_actions(state, moderator, game_state):
    parsed_player_actions: Dict[str, Action] = {}
    active_player_ids_from_moderator = moderator.get_active_player_ids()

    for sub_state, player in zip(state, game_state.players):
        player_id_str = player.id
        if player_id_str in active_player_ids_from_moderator and sub_state.status == "ACTIVE":
            serialized_action = sub_state.action
            if serialized_action:
                parsed_player_actions[player_id_str] = create_action(serialized_action)
    return parsed_player_actions

