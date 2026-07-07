DEFAULT_TRIGGER_RULES = {
    "prize_gap_threshold": 2,
    "opponent_confidence_threshold": 0.75,
    "turn_milestones": [3, 6, 9, 12, 15],
    "bench_count_min": 3,
    "bench_opponent_prizes_min": 3,
    "prized_attacker_threshold": 0.75,
}

DEFAULT_STRATEGY_SELECTION = {
    "prized_attacker_extreme_threshold": 0.99,
    "opponent_prizes_low": 2,
    "desperation_my_prizes_min": 5,
    "desperation_opponent_prizes_max": 3,
    "my_active_hp_critical": 30,
}

DEFAULT_HA_CONFIG = {
    "search_bench_mult": 0.1,
    "discard_draw_mult": 0.15,
    "discard_search_energy_mult": 0.25,
    "rare_candy_stage2_mult": 0.35,
    "supp_thresh": 2,
    "supp_factor": 0.1,
    "brick_factor": 0.15,
    "evo_match_factor": 0.20,
    "early_basic_bonus": 0.15,
    "early_supporter_bonus": 0.1,
    "mid_energy_bonus": 0.15,
    "mid_evolution_bonus": 0.1,
    "late_attacker_bonus": 0.15,
    "late_high_ev_threshold": 0.6,
    "late_high_ev_bonus": 0.1,
    "closing_opp_prizes": 2,
    "aggro_push_hand_score": 0.35,
    "setup_hand_score": 0.3,
    "disruption_control_count": 2,
    "disruption_opp_prizes": 3,
    "stall_deck_remaining": 15,
}
