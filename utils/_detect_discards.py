
def _detect_discards(belief_tracker, known_in_discard: dict):
    for cid, cnt in known_in_discard.items():
        prev_cnt = belief_tracker.state.known_in_discard.get(cid, 0)
        if cnt > prev_cnt:
            belief_tracker.update_on_discard(cid)


def _detect_discards(belief_tracker, known_in_discard: dict):
    for cid, cnt in known_in_discard.items():
        prev_cnt = belief_tracker.state.known_in_discard.get(cid, 0)
        if cnt > prev_cnt:
            belief_tracker.update_on_discard(cid)

