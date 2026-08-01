
def _track_actions(actions, strategy_trackers):
    pass_count = sum(1 for a in actions if "pass" in str(a).lower())
    strategy_trackers["passed_turns"] += pass_count
    stadium_wastes = sum(1 for a in actions if "play_trainer" in str(a).lower() and "stadium" in str(a).lower())
    strategy_trackers["stadium_wastes"] = strategy_trackers.get("stadium_wastes", 0) + (1 if stadium_wastes > 3 else 0)
    tool_plays = sum(1 for a in actions if "play_trainer" in str(a).lower() and "tool" in str(a).lower())
    strategy_trackers["tool_efficiency"] = strategy_trackers.get("tool_efficiency", 0) + tool_plays
    return pass_count

