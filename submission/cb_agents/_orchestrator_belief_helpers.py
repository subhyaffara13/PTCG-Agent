def get_id(obj):
    if obj is None:
        return None
    if isinstance(obj, (int, str)):
        try:
            return int(obj)
        except (ValueError, TypeError):
            return None
    if isinstance(obj, dict):
        val = obj.get("id")
        if val is not None:
            try:
                return int(val)
            except (ValueError, TypeError):
                pass
    for attr in ("id", "card_id"):
        if hasattr(obj, attr):
            val = getattr(obj, attr)
            if val is not None:
                try:
                    return int(val)
                except (ValueError, TypeError):
                    pass
    return None

def _detect_draw(belief_tracker, hand_size_diff: int):
    if hand_size_diff > 0:
        belief_tracker.update_on_draw(hand_size_diff)

def _detect_play(belief_tracker, known_in_play, active_id):
    prev_play = belief_tracker.state.known_in_play
    if active_id not in prev_play:
        belief_tracker.update_on_play(active_id)

def _detect_discards(belief_tracker, known_in_discard: dict):
    for cid, cnt in known_in_discard.items():
        prev_cnt = belief_tracker.state.known_in_discard.get(cid, 0)
        if cnt > prev_cnt:
            belief_tracker.update_on_discard(cid)
