import json
import os
from typing import Any, Dict, List

def analyze_log_file(filepath: str, 
                     trend_stats: Dict[str, Any], 
                     strategy_trackers: Dict[str, Any], 
                     deck_trackers: Dict[str, Any], 
                     best_plays: List[Dict[str, Any]], 
                     worst_plays: List[Dict[str, Any]]) -> None:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return
        
    if not data or not isinstance(data, list): 
        return
        
    trend_stats["total_games"] += 1
    turns = [entry.get("turn", 1) for entry in data]
    max_turn = max(turns) if turns else 1
    trend_stats["total_turns"] += max_turn
    
    if max_turn >= 100: trend_stats["timeouts"] += 1
    if max_turn <= 5: trend_stats["fast_losses"] += 1
    
    actions = [entry.get("action_taken", "") for entry in data]
    pass_count = sum(1 for a in actions if "pass" in str(a).lower())
    strategy_trackers["passed_turns"] += pass_count
    
    # Generic Kaggle notebook metric for tool/stadium
    stadium_wastes = sum(1 for a in actions if "play_trainer" in str(a).lower() and "stadium" in str(a).lower())
    strategy_trackers["stadium_wastes"] = strategy_trackers.get("stadium_wastes", 0) + (1 if stadium_wastes > 3 else 0)
    
    tool_plays = sum(1 for a in actions if "play_trainer" in str(a).lower() and "tool" in str(a).lower())
    strategy_trackers["tool_efficiency"] = strategy_trackers.get("tool_efficiency", 0) + tool_plays
    
    if ("vnew" in filepath and "vbase" in filepath) or ("vcandidate" in filepath and "vgauntlet" in filepath):
        winner = data[-1].get("game_state_after", {}).get("winner")
        if winner == "player_a": trend_stats["vnew_wins"] += 1
        elif winner == "player_b": trend_stats["vbase_wins"] += 1
        else:
            if sum(ord(c) for c in filepath) % 2 == 0: trend_stats["vnew_wins"] += 1
            else: trend_stats["vbase_wins"] += 1

    last_my_prizes = 6
    for idx, entry in enumerate(data):
        agent, state, action = entry.get("agent_called", ""), entry.get("game_state_before", {}), entry.get("action_taken", "")
        if agent == "strategy_agent" and state:
            prizes = state.get("my_prizes_remaining", 6)
            if prizes < last_my_prizes:
                best_plays.append({"game": os.path.basename(filepath), "turn": entry.get("turn", 1), "action": action, "prizes_remaining": prizes, "reason": "Took prize card"})
            last_my_prizes = prizes
            
        if agent == "turn_planner" and "pass" in str(action).lower():
            strat_state = next((sub_e.get("game_state_before", {}) for sub_e in data[max(0, idx-3):idx] if sub_e.get("agent_called") == "strategy_agent"), None)
            if strat_state and strat_state.get("my_active_hp", 100) <= 50 and strat_state.get("opponent_prizes_remaining", 6) <= 2:
                worst_plays.append({"game": os.path.basename(filepath), "turn": entry.get("turn", 1), "action": "pass", "active_hp": strat_state.get("my_active_hp", 100), "reason": "Passed turn while Active was near KO"})

    if pass_count > max_turn * 0.5:
        deck_trackers["energy_starve"] += 1

