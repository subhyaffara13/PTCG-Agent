from typing import List, Dict, Any
from factory.parallel_runner_pool import GameResult

def compute_summary(results: List[GameResult]) -> Dict[str, Any]:
    total = len(results)
    successes = sum(1 for r in results if r.success)
    win_counts = {"player_a": 0, "player_b": 0, "draw": 0, "error": 0}
    total_turns, games_with_turns = 0, 0
    for r in results:
        if not r.success or not r.result:
            win_counts["error"] += 1
            continue
        for game_data in r.result.get("games", {}).values():
            winner = game_data.get("winner", "error")
            win_counts[winner] = win_counts.get(winner, 0) + 1
            turns = game_data.get("turns_taken", 0)
            if turns > 0:
                total_turns += turns
                games_with_turns += 1
    avg = round(total_turns / games_with_turns, 1) if games_with_turns > 0 else 0
    return {
        "total_games": total, "successes": successes, "failures": total - successes,
        "win_distribution": win_counts, "avg_turns": avg
    }
