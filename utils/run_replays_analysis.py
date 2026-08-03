import json
from typing import List
from pathlib import Path


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
                    from factory.anti_pattern_extractor_helpers import extract_deck_anti_patterns
                    extract_deck_anti_patterns(deck, extractor.learned_donts, extractor._save_donts)
            
            formatted_steps = []
            for s in steps:
                formatted_steps.append({"players": s})
                
            bv = compute_from_steps(formatted_steps, player_idx)
            from factory.anti_pattern_extractor_helpers import extract_behavior_anti_patterns
            extract_behavior_anti_patterns(bv, extractor.learned_donts, extractor._save_donts)
        except Exception as e:
            logger.error(f"Error parsing replay {path} for anti-patterns: {e}")

