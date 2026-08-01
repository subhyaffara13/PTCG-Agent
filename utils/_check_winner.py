
def _check_winner(filepath, data, trend_stats):
    if ("vnew" in filepath and "vbase" in filepath) or ("vcandidate" in filepath and "vgauntlet" in filepath):
        winner = data[-1].get("game_state_after", {}).get("winner")
        if winner == "player_a": trend_stats["vnew_wins"] += 1
        elif winner == "player_b": trend_stats["vbase_wins"] += 1
        else:
            if sum(ord(c) for c in filepath) % 2 == 0: trend_stats["vnew_wins"] += 1
            else: trend_stats["vbase_wins"] += 1

