
def _load_game_result(args):
    file_path, preserve_full_record = args
    game_json = _load_json(file_path)
    if game_json is None:
        raise ValueError(f"Failed to load JSON from {file_path}")
    return GameResult(game_json, preserve_full_record=preserve_full_record)

