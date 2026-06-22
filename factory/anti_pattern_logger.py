import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger("AntiPatternHelper")

def load_donts(donts_file: Path) -> Dict[str, Any]:
    data = {
        "deck_donts": [],
        "behavior_donts": []
    }
    if donts_file.exists():
        try:
            loaded = json.loads(donts_file.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                data.update(loaded)
        except json.JSONDecodeError:
            pass
    if "deck_donts" not in data:
        data["deck_donts"] = []
    if "behavior_donts" not in data:
        data["behavior_donts"] = []
    return data

def save_donts(donts_file: Path, learned_donts: dict):
    try:
        donts_file.write_text(json.dumps(learned_donts, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to save learned don'ts: {e}")

def run_replays_analysis(replay_paths: List[Path], player_name_or_id: str, extractor) -> None:
    from factory.behavioral_features import compute_from_steps
    for path in replay_paths:
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            steps = data.get("steps", [])
            rewards = data.get("rewards", [0, 0])
            info = data.get("info", {})
            team_names = info.get("TeamNames", ["", ""])
            
            player_idx = -1
            if str(player_name_or_id).isdigit():
                if len(steps) > 1:
                    for idx, p_state in enumerate(steps[1]):
                        obs_dict = p_state.get("observation") or {} if p_state else {}
                        current = obs_dict.get("current") or {} if obs_dict else {}
                        players = current.get("players", []) if current else []
                        if idx < len(players) and str(players[idx].get("teamId")) == str(player_name_or_id):
                            player_idx = idx
                            break
            else:
                for idx, name in enumerate(team_names):
                    if player_name_or_id.lower() in name.lower():
                        player_idx = idx
                        break
                        
            if player_idx == -1 or len(rewards) <= player_idx:
                continue
                
            if rewards[player_idx] >= 0:
                continue
            
            if len(steps) > 1 and len(steps[1]) > player_idx:
                deck = steps[1][player_idx].get("action", [])
                if len(deck) == 60:
                    extractor._extract_deck_anti_patterns(deck)
            
            formatted_steps = []
            for s in steps:
                formatted_steps.append({"players": s})
                
            bv = compute_from_steps(formatted_steps, player_idx)
            extractor._extract_behavior_anti_patterns(bv)
        except Exception as e:
            logger.error(f"Error parsing replay {path} for anti-patterns: {e}")
