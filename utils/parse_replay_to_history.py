
def parse_replay_to_history(replay_path) -> List[Dict[str, Any]]:
    import json, logging
    logger = logging.getLogger(__name__)
    if not replay_path or not replay_path.exists():
        return []
    try:
        data = json.loads(replay_path.read_text(encoding="utf-8"))
        steps = data.get("steps", [])
        history = []
        for turn_idx, step in enumerate(steps, start=1):
            for idx, player_state in enumerate(step):
                obs = player_state.get("observation", {}) or {}
                history.append({
                    "turn": turn_idx, "player_index": idx,
                    "action_taken": player_state.get("action", []),
                    "reward": player_state.get("reward", 0),
                    "status": player_state.get("status", "ACTIVE"),
                    "my_prizes_remaining": obs.get("my_prizes", 6),
                    "opponent_prizes_remaining": obs.get("opponent_prizes", 6),
                    "my_active_hp": obs.get("my_active_hp", 100),
                    "opponent_active_hp": obs.get("opponent_active_hp", 100)
                })
        return history
    except Exception as e:
        logger.error(f"Failed to parse replay file {replay_path}: {e}")
        return []

