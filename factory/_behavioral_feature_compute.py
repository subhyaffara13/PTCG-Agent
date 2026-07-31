from typing import List, Dict
from factory.behavioral_features import BehavioralVector

def compute_per_turn_metrics(steps, player_idx):
    turns = len(steps)
    total_energy = 0
    disruptive = 0
    total_trainer = 0
    setup_duration = turns
    bench_counts = []
    hand_scores = []
    initial_prizes = 6
    final_prizes = 6
    for i, step in enumerate(steps):
        try:
            player_state = step["players"][player_idx]
            if not player_state:
                continue
            obs_dict = player_state.get("observation") or {}
            obs = obs_dict.get("current") or {}
            if not obs:
                continue
            players = obs.get("players", [])
            if len(players) <= player_idx:
                continue
            p_data = players[player_idx]
            if i == 0:
                initial_prizes = len(p_data.get("prize", []))
            final_prizes = len(p_data.get("prize", []))
            bench = p_data.get("bench", [])
            bench_counts.append(len(bench))
            action_indices = player_state.get("action")
            if isinstance(action_indices, list) and action_indices:
                chosen_idx = action_indices[0]
                select = obs_dict.get("select") or {}
                options = select.get("options") or select.get("option") or []
                if isinstance(options, list) and 0 <= chosen_idx < len(options):
                    chosen_option = options[chosen_idx]
                    opt_type = chosen_option.get("type")
                    if opt_type == 13:
                        if setup_duration == turns:
                            setup_duration = i
                    elif opt_type == 9:
                        total_energy += 1
                    elif opt_type == 7:
                        total_trainer += 1
                        opt_name = str(chosen_option.get("name", "")).lower()
                        if any(k in opt_name for k in ["judge", "marnie", "red card", "hand disruption", "disrupt"]):
                            disruptive += 1
            hand_size = len(p_data.get("hand", []))
            hand_scores.append(hand_size / 7.0)
        except Exception:
            pass
    return {
        "turns": turns, "initial_prizes": initial_prizes, "final_prizes": final_prizes,
        "total_energy": total_energy, "disruptive": disruptive, "total_trainer": total_trainer,
        "setup_duration": setup_duration, "bench_counts": bench_counts, "hand_scores": hand_scores
    }

def build_behavioral_vector(m):
    import math
    prize_diff = max(0, m["initial_prizes"] - m["final_prizes"])
    turn_aggro = prize_diff / max(1, m["turns"])
    energy_accel = m["total_energy"] / max(1, m["turns"])
    hand_disruption = m["disruptive"] / max(1, m["total_trainer"])
    bench_density = sum(m["bench_counts"]) / max(1, len(m["bench_counts"]))
    avg_score = sum(m["hand_scores"]) / max(1, len(m["hand_scores"]))
    variance = sum((x - avg_score) ** 2 for x in m["hand_scores"]) / max(1, len(m["hand_scores"]))
    consistency = max(0.0, 1.0 - math.sqrt(variance))
    return BehavioralVector(
        turn_aggro=turn_aggro, energy_accel_rate=energy_accel,
        hand_disruption=hand_disruption, setup_duration=m["setup_duration"],
        bench_density=bench_density, evolution_depth=0.0, consistency=consistency
    )
