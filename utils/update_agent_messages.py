
def update_agent_messages(
    state, env, moderator, game_state, is_game_done, current_info, active_player_ids_after_advance, agent_error
):
    for player_index, player_state in enumerate(state):
        player_id_str = env.player_ids_map[player_index]

        # skip if player not active and game is not done
        if player_id_str not in active_player_ids_after_advance and not is_game_done:
            player_state.status = "INACTIVE"
            continue

        # set the status of active player to ACTIVE
        player_state.status = "ACTIVE"
        player_obj = game_state.get_player_by_id(player_id_str)

        # Observation processing
        new_history_entries = player_obj.consume_messages()

        obs = WerewolfObservationModel(
            player_id=player_obj.id,
            role=player_obj.role.name,
            team=player_obj.role.team.value,
            is_alive=player_obj.alive,
            day=game_state.day_count,
            detailed_phase=moderator.detailed_phase.value,
            all_player_ids=game_state.all_player_ids,
            player_thumbnails=env.player_thumbnails,
            alive_players=[p.id for p in game_state.alive_players()],
            revealed_players=game_state.revealed_players(),
            new_visible_announcements=[entry.description for entry in new_history_entries],
            new_player_event_views=new_history_entries,
            game_state_phase=game_state.phase.value,
        )

        set_raw_observation(player_state, raw_obs=obs)

        # Status
        if is_game_done or agent_error:
            player_state.status = "DONE"
        elif player_id_str in active_player_ids_after_advance:
            player_state.status = "ACTIVE"
        else:
            player_state.status = "INACTIVE"

        # Info
        player_state.info = current_info

