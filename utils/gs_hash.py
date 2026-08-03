import json

def gs_hash(game_state: dict) -> int:
    """Compute a deterministic hash for a game state dict for transposition detection."""
    try:
        key_parts = []
        for k in sorted(game_state.keys()):
            if k in ("legal_actions", "turn_ended", "game_over", "winner", "reasoning_chain"):
                continue
            v = game_state[k]
            try:
                json.dumps(v)
                key_parts.append((k, str(v)))
            except (TypeError, ValueError):
                pass
        return int(hashlib.sha256(str(tuple(key_parts)).encode()).hexdigest()[:16], 16)
    except Exception:
        return 0


def gs_hash(game_state: dict) -> int:
    """Compute a deterministic hash for a game state dict for transposition detection."""
    try:
        key_parts = []
        for k in sorted(game_state.keys()):
            if k in ("legal_actions", "turn_ended", "game_over", "winner", "reasoning_chain"):
                continue
            v = game_state[k]
            try:
                json.dumps(v)
                key_parts.append((k, str(v)))
            except (TypeError, ValueError):
                pass
        return int(hashlib.sha256(str(tuple(key_parts)).encode()).hexdigest()[:16], 16)
    except Exception:
        return 0

