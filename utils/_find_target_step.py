
def _find_target_step(steps):
    target_step = None
    for step in steps:
        if isinstance(step, list):
            players = step
        elif isinstance(step, dict):
            players = step.get("players", [])
        else:
            continue
        if not players or not isinstance(players[0], dict): continue
        obs = players[0].get("observation") or {}
        curr = obs.get("current") or {}
        turn = curr.get("turn", 1)
        if turn is not None and 3 <= turn <= 5: target_step = step
        if turn is not None and turn > 5: break
    if not target_step and steps: target_step = steps[-1]
    if not target_step: return None, []
    if isinstance(target_step, list): players_state = target_step
    elif isinstance(target_step, dict): players_state = target_step.get("players", [])
    else: return None, []
    return target_step, players_state

