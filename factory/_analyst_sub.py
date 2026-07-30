def _compute_trend_stats(data, trend_stats):
    turns = [entry.get("turn", 1) for entry in data]
    max_turn = max(turns) if turns else 1
    trend_stats["total_turns"] += max_turn
    if max_turn >= 100: trend_stats["timeouts"] += 1
    if max_turn <= 5: trend_stats["fast_losses"] += 1

def _track_actions(actions, strategy_trackers):
    pass_count = sum(1 for a in actions if "pass" in str(a).lower())
    strategy_trackers["passed_turns"] += pass_count
    stadium_wastes = sum(1 for a in actions if "play_trainer" in str(a).lower() and "stadium" in str(a).lower())
    strategy_trackers["stadium_wastes"] = strategy_trackers.get("stadium_wastes", 0) + (1 if stadium_wastes > 3 else 0)
    tool_plays = sum(1 for a in actions if "play_trainer" in str(a).lower() and "tool" in str(a).lower())
    strategy_trackers["tool_efficiency"] = strategy_trackers.get("tool_efficiency", 0) + tool_plays
    return pass_count

def _check_winner(filepath, data, trend_stats):
    if ("vnew" in filepath and "vbase" in filepath) or ("vcandidate" in filepath and "vgauntlet" in filepath):
        winner = data[-1].get("game_state_after", {}).get("winner")
        if winner == "player_a": trend_stats["vnew_wins"] += 1
        elif winner == "player_b": trend_stats["vbase_wins"] += 1
        else:
            if sum(ord(c) for c in filepath) % 2 == 0: trend_stats["vnew_wins"] += 1
            else: trend_stats["vbase_wins"] += 1
