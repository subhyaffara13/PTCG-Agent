import math
from typing import List, Dict, Any
from factory.behavioral_features import BehavioralVector
from factory.diversity_tracker import DiversityTracker  # Expose for backward compatibility

def compute_from_steps(steps: List[Dict], player_idx: int) -> BehavioralVector:
    """
    Computes a BehavioralVector for a specific player based on game replay steps.
    """
    if not steps:
        return BehavioralVector(0, 0, 0, 0, 0, 0, 0)

    turns = len(steps)
    total_energy_attached = 0
    disruptive_plays = 0
    total_trainer_plays = 0
    setup_duration = turns
    bench_counts = []
    max_evolution = 0
    hand_scores = []
    
    initial_prizes = 6
    final_prizes = 6

    # Track metrics per turn
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
            
            # Prizes
            if i == 0:
                initial_prizes = len(p_data.get("prize", []))
            final_prizes = len(p_data.get("prize", []))
            
            # Bench density
            bench = p_data.get("bench", [])
            bench_counts.append(len(bench))
            
            # Setup duration and energy/trainer play tracking by parsing options at index
            action_indices = player_state.get("action")
            if isinstance(action_indices, list) and action_indices:
                chosen_idx = action_indices[0]
                select = obs_dict.get("select") or {}
                options = select.get("options") or select.get("option") or []
                if isinstance(options, list) and 0 <= chosen_idx < len(options):
                    chosen_option = options[chosen_idx]
                    opt_type = chosen_option.get("type")
                    if opt_type == 13: # Attack
                        if setup_duration == turns:
                            setup_duration = i
                    elif opt_type == 9: # Energy attachment
                        total_energy_attached += 1
                    elif opt_type == 7: # Trainer play
                        total_trainer_plays += 1
                        opt_name = str(chosen_option.get("name", "")).lower()
                        if any(k in opt_name for k in ["judge", "marnie", "red card", "hand disruption", "disrupt"]):
                            disruptive_plays += 1
                            
            # Hand consistency (we'll just use hand size as a proxy if scores aren't in steps)
            hand_size = len(p_data.get("hand", []))
            hand_scores.append(hand_size / 7.0)  # rough normalization
                    
        except Exception:
            pass

    prize_diff = max(0, initial_prizes - final_prizes)
    turn_aggro = prize_diff / max(1, turns)
    energy_accel = total_energy_attached / max(1, turns)
    hand_disruption = disruptive_plays / max(1, total_trainer_plays)
    bench_density = sum(bench_counts) / max(1, len(bench_counts))
    
    # Consistency calculation
    avg_score = sum(hand_scores) / max(1, len(hand_scores))
    variance = sum((x - avg_score)**2 for x in hand_scores) / max(1, len(hand_scores))
    consistency = max(0.0, 1.0 - math.sqrt(variance))

    return BehavioralVector(
        turn_aggro=turn_aggro,
        energy_accel_rate=energy_accel,
        hand_disruption=hand_disruption,
        setup_duration=setup_duration,
        bench_density=bench_density,
        evolution_depth=float(max_evolution),
        consistency=consistency
    )
