
def _collect_board_pokemon_names(observation):
    board_pokemon_names = set()
    try:
        current = observation.get("current")
        if current is None:
            return board_pokemon_names
        my_idx = current.get("yourIndex", 0)
        players = current.get("players", [])
        if not (len(players) > my_idx and players[my_idx] is not None):
            return board_pokemon_names
        my_state = players[my_idx]
        act = _resolve_instance(my_state.get("active"))
        if act:
            act_name = act.get("name")
            if not act_name and act.get("card"):
                act_name = act.get("card").get("name")
            if act_name:
                board_pokemon_names.add(str(act_name).lower())
        for b in my_state.get("bench", []):
            b_resolved = _resolve_instance(b)
            if b_resolved:
                b_name = b_resolved.get("name")
                if not b_name and b_resolved.get("card"):
                    b_name = b_resolved.get("card").get("name")
                if b_name:
                    board_pokemon_names.add(str(b_name).lower())
    except Exception:
        pass
    return board_pokemon_names

