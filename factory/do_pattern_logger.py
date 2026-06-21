import json
import logging
from pathlib import Path
from collections import Counter
from typing import List, Dict, Any

logger = logging.getLogger("DoPatternLogger")

def load_dos(dos_file: Path) -> Dict[str, Any]:
    if dos_file.exists():
        try:
            return json.loads(dos_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "deck_dos": [],
        "behavior_dos": [],
        "deck_stats": {}
    }

def save_dos(dos_file: Path, learned_dos: dict):
    try:
        dos_file.write_text(json.dumps(learned_dos, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to save learned do's: {e}")

def run_winning_analysis(replay_paths: List[Path], player_name_or_id: str, extractor) -> None:
    card_counter = Counter()
    setup_durations = []
    bench_densities = []
    pokemon_counts = []
    trainer_counts = []
    energy_counts = []
    total_wins = 0

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
                
            if rewards[player_idx] <= 0:
                continue
            
            total_wins += 1
            
            if len(steps) > 1 and len(steps[1]) > player_idx:
                deck = steps[1][player_idx].get("action", [])
                if len(deck) == 60:
                    card_counter.update(deck)
                    
                    from agents.card_registry import CardRegistry
                    from agents.card_types import CardType
                    registry = CardRegistry()
                    
                    p_c = 0
                    t_c = 0
                    e_c = 0
                    for cid in deck:
                        c = registry.get(cid)
                        if c:
                            if c.card_type == CardType.POKEMON: p_c += 1
                            elif c.card_type == CardType.TRAINER: t_c += 1
                            elif c.card_type == CardType.ENERGY: e_c += 1
                        else:
                            if cid <= 20:
                                e_c += 1
                            else:
                                t_c += 1
                    pokemon_counts.append(p_c)
                    trainer_counts.append(t_c)
                    energy_counts.append(e_c)
            
            setup_dur = len(steps)
            bench_sizes = []
            for turn_idx, step in enumerate(steps):
                if len(step) > player_idx:
                    p_state = step[player_idx]
                    obs_dict = p_state.get("observation") or {} if p_state else {}
                    obs = obs_dict.get("current") or {} if obs_dict else {}
                    if obs and "players" in obs:
                        p_data = obs["players"][player_idx]
                        bench = p_data.get("bench", [])
                        bench_sizes.append(len(bench))
                        
                    action = step[player_idx].get("action", [])
                    if action and isinstance(action, list) and len(action) > 0:
                        if action[0] == 2:
                            if setup_dur == len(steps):
                                setup_dur = turn_idx
                                
            setup_durations.append(setup_dur)
            if bench_sizes:
                bench_densities.append(sum(bench_sizes) / len(bench_sizes))
        except Exception as e:
            logger.error(f"Error parsing replay {path} for do-patterns: {e}")

    if total_wins == 0:
        logger.info("No winning replays processed for do-patterns.")
        return

    deck_dos = []
    for card_id, count in card_counter.items():
        avg_count = count / total_wins
        if avg_count >= 1.5:
            deck_dos.append({
                "card_id": int(card_id),
                "avg_count": round(avg_count, 2),
                "reason": f"High usage ({round(avg_count, 1)}x avg) in winning matches of player {player_name_or_id}."
            })
    
    for new_do in deck_dos:
        existing = next((item for item in extractor.learned_dos["deck_dos"] if item["card_id"] == new_do["card_id"]), None)
        if existing:
            existing["avg_count"] = max(existing.get("avg_count", 0), new_do["avg_count"])
        else:
            extractor.learned_dos["deck_dos"].append(new_do)

    if setup_durations:
        avg_setup = sum(setup_durations) / len(setup_durations)
        avg_bench = sum(bench_densities) / len(bench_densities) if bench_densities else 0.0
        behavior_do = {
            "player": str(player_name_or_id),
            "avg_setup_duration": round(avg_setup, 1),
            "avg_bench_density": round(avg_bench, 1)
        }
        extractor.learned_dos["behavior_dos"] = [
            b for b in extractor.learned_dos["behavior_dos"] if b["player"] != str(player_name_or_id)
        ]
        extractor.learned_dos["behavior_dos"].append(behavior_do)

    if pokemon_counts:
        avg_poke = sum(pokemon_counts) / len(pokemon_counts)
        avg_train = sum(trainer_counts) / len(trainer_counts)
        avg_energy = sum(energy_counts) / len(energy_counts)
        extractor.learned_dos["deck_stats"] = {
            "avg_pokemon_count": round(avg_poke, 1),
            "avg_trainer_count": round(avg_train, 1),
            "avg_energy_count": round(avg_energy, 1)
        }

    extractor._save_dos()
    logger.info(f"Extracted {len(deck_dos)} deck recommendations from {total_wins} winning matches.")
