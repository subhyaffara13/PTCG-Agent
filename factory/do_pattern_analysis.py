import json
import logging
from pathlib import Path
from collections import Counter
from typing import List

logger = logging.getLogger("DoPatternAnalysis")

def _get_player_idx(steps, info, team_names, name_or_id) -> int:
    if str(name_or_id).isdigit():
        if len(steps) > 1:
            for idx, p_state in enumerate(steps[1]):
                obs = p_state.get("observation") or {} if p_state else {}
                players = (obs.get("current") or {}).get("players", [])
                if idx < len(players) and str(players[idx].get("teamId")) == str(name_or_id):
                    return idx
    else:
        for idx, name in enumerate(team_names):
            if name_or_id.lower() in name.lower():
                return idx
    return -1

def _count_deck_types(deck) -> tuple:
    from cb_agents.card_registry import CardRegistry
    from cb_agents.card_types import CardType
    reg = CardRegistry()
    p_c, t_c, e_c = 0, 0, 0
    for cid in deck:
        c = reg.get(cid)
        if c:
            if c.card_type == CardType.POKEMON: p_c += 1
            elif c.card_type == CardType.TRAINER: t_c += 1
            elif c.card_type == CardType.ENERGY: e_c += 1
        else:
            if cid <= 20: e_c += 1
            else: t_c += 1
    return p_c, t_c, e_c

def _process_replay_steps(steps, player_idx, card_counter, setup_durations, bench_densities, p_counts, t_counts, e_counts):
    if len(steps) > 1 and len(steps[1]) > player_idx:
        deck = steps[1][player_idx].get("action", [])
        if len(deck) == 60:
            card_counter.update(deck)
            p_c, t_c, e_c = _count_deck_types(deck)
            p_counts.append(p_c); t_counts.append(t_c); e_counts.append(e_c)
            
    setup_dur, bench_sizes = len(steps), []
    for turn_idx, step in enumerate(steps):
        if len(step) > player_idx:
            obs = (step[player_idx].get("observation") or {}).get("current") or {}
            if obs and "players" in obs:
                bench_sizes.append(len(obs["players"][player_idx].get("bench", [])))
            act = step[player_idx].get("action", [])
            if act and isinstance(act, list) and len(act) > 0 and act[0] == 2 and setup_dur == len(steps):
                setup_dur = turn_idx
    setup_durations.append(setup_dur)
    if bench_sizes: bench_densities.append(sum(bench_sizes) / len(bench_sizes))

def run_winning_analysis(replay_paths: List[Path], player_name_or_id: str, extractor) -> None:
    card_counter = Counter()
    setup_durs, bench_dens, p_counts, t_counts, e_counts = [], [], [], [], []
    total_wins = 0

    for path in replay_paths:
        if not path.exists(): continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            steps = data.get("steps", [])
            player_idx = _get_player_idx(steps, data.get("info", {}), data.get("info", {}).get("TeamNames", ["", ""]), player_name_or_id)
            if player_idx == -1 or len(data.get("rewards", [])) <= player_idx or data.get("rewards", [])[player_idx] <= 0:
                continue
            total_wins += 1
            _process_replay_steps(steps, player_idx, card_counter, setup_durs, bench_dens, p_counts, t_counts, e_counts)
        except Exception as e:
            logger.error(f"Error parsing replay {path}: {e}")

    if total_wins == 0: return

    deck_dos = [{"card_id": int(cid), "avg_count": round(cnt / total_wins, 2), "reason": f"High usage in winning matches."}
                for cid, cnt in card_counter.items() if (cnt / total_wins) >= 1.5]
                
    for new_do in deck_dos:
        existing = next((item for item in extractor.learned_dos["deck_dos"] if item["card_id"] == new_do["card_id"]), None)
        if existing: existing["avg_count"] = max(existing.get("avg_count", 0), new_do["avg_count"])
        else: extractor.learned_dos["deck_dos"].append(new_do)

    if setup_durs:
        behavior_do = {"player": str(player_name_or_id), "avg_setup_duration": round(sum(setup_durs)/len(setup_durs), 1),
                       "avg_bench_density": round(sum(bench_dens)/len(bench_dens) if bench_dens else 0.0, 1)}
        extractor.learned_dos["behavior_dos"] = [b for b in extractor.learned_dos["behavior_dos"] if b["player"] != str(player_name_or_id)] + [behavior_do]

    if p_counts:
        extractor.learned_dos["deck_stats"] = {"avg_pokemon_count": round(sum(p_counts)/len(p_counts), 1),
                                               "avg_trainer_count": round(sum(t_counts)/len(t_counts), 1),
                                               "avg_energy_count": round(sum(e_counts)/len(e_counts), 1)}
    extractor._save_dos()
    logger.info(f"Extracted {len(deck_dos)} deck recommendations from {total_wins} matches.")
