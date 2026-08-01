
def _safe_load_game_result(args):
    try:
        return _load_game_result(args), None
    except Exception as e:
        return None, e

