
def _detect_play(belief_tracker, known_in_play, active_id):
    prev_play = belief_tracker.state.known_in_play
    if active_id not in prev_play:
        belief_tracker.update_on_play(active_id)


def _detect_play(belief_tracker, known_in_play, active_id):
    prev_play = belief_tracker.state.known_in_play
    if active_id not in prev_play:
        belief_tracker.update_on_play(active_id)

