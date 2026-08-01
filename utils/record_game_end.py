
def record_game_end(state, env, game_state, current_info, agent_error):
    # log game end to env.info using GameEndResultsDataEntry
    game_end_entry = next(iter(game_state.get_event_by_name(EventName.GAME_END)), None)
    if game_end_entry and game_end_entry.data:
        current_info.update(game_end_entry.data.model_dump())
    # Record if terminated with agent error. If so, the game record is invalid.
    current_info["terminated_with_agent_error"] = agent_error

    # Record cost from endpoints if any.
    # current_info["cost_summary"] = collect_cost_summary(env).model_dump()

    env.info[EnvInfoKeys.GAME_END] = current_info
    # Determine winner based on game_state.history's GAME_END entry
    if game_end_entry:
        scores = game_end_entry.data.scores
        for i, player_id in enumerate(env.player_id_str_list):
            state[i].reward = scores[player_id]

