import json

from utils.make_card_scoring import make_card_scoring

INITIAL_THRESHOLDS = {
    "hand_analyst": {
        "combo_multipliers": {"search_and_bench": 0.1, "discard_and_draw": 0.15, "discard_search_energy": 0.25, "rare_candy_stage2": 0.35},
        "penalties": {"supporter_oversaturation_threshold": 2, "supporter_oversaturation_factor": 0.1, "brick_factor": 0.15},
        "bonuses": {"evolution_match_factor": 0.20, "early_basic": 0.15, "early_supporter": 0.1, "mid_energy": 0.15, "mid_evolution": 0.1, "late_attacker": 0.15, "late_high_ev_threshold": 0.6, "late_high_ev_bonus": 0.1},
        "priority_profiles": {"closing": {"opponent_prizes_max": 2}, "aggro_push": {"hand_score_min": 0.35}, "setup": {"hand_score_max": 0.3}, "disruption": {"control_count_min": 2, "opponent_prizes_max": 3}, "stall": {"deck_remaining_max": 15}}
    },
    "strategy_agent": {
        "trigger_rules": {"prize_gap_threshold": 2, "opponent_confidence_threshold": 0.75, "turn_milestones": [3, 6, 9, 12, 15], "bench_count_min": 3, "bench_opponent_prizes_min": 3, "prized_attacker_threshold": 0.75},
        "strategy_selection": {"prized_attacker_extreme_threshold": 0.99, "opponent_prizes_low": 2, "desperation_my_prizes_min": 5, "desperation_opponent_prizes_max": 3, "my_active_hp_critical": 30}
    }
}

MODIFIED_THRESHOLDS = {
    "hand_analyst": {
        "combo_multipliers": {"search_and_bench": 5.0, "discard_and_draw": 0.15, "discard_search_energy": 0.25, "rare_candy_stage2": 0.35},
        "penalties": {"supporter_oversaturation_threshold": 2, "supporter_oversaturation_factor": 0.1, "brick_factor": 0.15},
        "bonuses": {"evolution_match_factor": 0.20, "early_basic": 0.15, "early_supporter": 0.1, "mid_energy": 0.15, "mid_evolution": 0.1, "late_attacker": 0.15, "late_high_ev_threshold": 0.6, "late_high_ev_bonus": 0.1},
        "priority_profiles": {"closing": {"opponent_prizes_max": 2}, "aggro_push": {"hand_score_min": 0.35}, "setup": {"hand_score_max": 0.3}, "disruption": {"control_count_min": 2, "opponent_prizes_max": 3}, "stall": {"deck_remaining_max": 15}}
    },
    "strategy_agent": {
        "trigger_rules": {"prize_gap_threshold": 5, "opponent_confidence_threshold": 0.75, "turn_milestones": [3, 6, 9, 12, 15], "bench_count_min": 3, "bench_opponent_prizes_min": 3, "prized_attacker_threshold": 0.75},
        "strategy_selection": {"prized_attacker_extreme_threshold": 0.99, "opponent_prizes_low": 2, "desperation_my_prizes_min": 5, "desperation_opponent_prizes_max": 3, "my_active_hp_critical": 30}
    }
}
