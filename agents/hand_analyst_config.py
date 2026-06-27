from typing import Dict, Any
from agents.configs import DEFAULT_HA_CONFIG

SECTION_MAP = [
    ("combo_multipliers", "search_and_bench", "search_bench_mult"),
    ("combo_multipliers", "discard_and_draw", "discard_draw_mult"),
    ("combo_multipliers", "discard_search_energy", "discard_search_energy_mult"),
    ("combo_multipliers", "rare_candy_stage2", "rare_candy_stage2_mult"),
    ("penalties", "supporter_oversaturation_threshold", "supp_thresh"),
    ("penalties", "supporter_oversaturation_factor", "supp_factor"),
    ("penalties", "brick_factor", "brick_factor"),
    ("bonuses", "evolution_match_factor", "evo_match_factor"),
    ("bonuses", "early_basic", "early_basic_bonus"),
    ("bonuses", "early_supporter", "early_supporter_bonus"),
    ("bonuses", "mid_energy", "mid_energy_bonus"),
    ("bonuses", "mid_evolution", "mid_evolution_bonus"),
    ("bonuses", "late_attacker", "late_attacker_bonus"),
    ("bonuses", "late_high_ev_threshold", "late_high_ev_threshold"),
    ("bonuses", "late_high_ev_bonus", "late_high_ev_bonus"),
]

PROFILE_MAP = [
    ("closing", "opponent_prizes_max", "closing_opp_prizes"),
    ("aggro_push", "hand_score_min", "aggro_push_hand_score"),
    ("setup", "hand_score_max", "setup_hand_score"),
    ("disruption", "control_count_min", "disruption_control_count"),
    ("disruption", "opponent_prizes_max", "disruption_opp_prizes"),
    ("stall", "deck_remaining_max", "stall_deck_remaining"),
]

def unpack_ha_config(strategy_thresholds: Dict[str, Any]) -> dict:
    ha_config = strategy_thresholds.get("hand_analyst", {}) if isinstance(strategy_thresholds, dict) else {}
    if not isinstance(ha_config, dict):
        return dict(DEFAULT_HA_CONFIG)
    
    result = dict(DEFAULT_HA_CONFIG)
    for section, src_key, dst_key in SECTION_MAP:
        sub = ha_config.get(section, {})
        if isinstance(sub, dict) and src_key in sub:
            result[dst_key] = sub[src_key]
    
    profiles = ha_config.get("priority_profiles", {})
    if isinstance(profiles, dict):
        for profile, src_key, dst_key in PROFILE_MAP:
            psub = profiles.get(profile, {})
            if isinstance(psub, dict) and src_key in psub:
                result[dst_key] = psub[src_key]
    return result
