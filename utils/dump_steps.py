
def dump_steps(raw_steps: list) -> list:
    steps_dump = []
    for idx, step in enumerate(raw_steps or []):
        step_data = []
        for player_idx, player_state in enumerate(step or []):
            if player_state is None:
                player_state = {}
            clean_obs = {k: v for k, v in player_state.get("observation", {}).items() if k != "search_begin_input"}
            step_data.append({
                "action": player_state.get("action"),
                "reward": player_state.get("reward"),
                "status": player_state.get("status"),
                "observation": clean_obs
            })
        steps_dump.append(step_data)
    return steps_dump

