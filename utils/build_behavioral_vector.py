
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

