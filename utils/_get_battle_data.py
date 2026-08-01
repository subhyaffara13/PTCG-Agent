
def _get_battle_data() -> dict:
    """Retrieve the current state.

    Returns:
        dict: Current observation.
    """
    sd = lib.GetBattleData(Battle.battle_ptr)
    Battle.obs = json.loads(sd.json.decode())
    Battle.obs["search_begin_input"] = ctypes.string_at(sd.data, sd.count).decode("ascii")
    return Battle.obs

