from typing import Dict, Any
from cb_agents.configs import DEFAULT_HA_CONFIG

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

from utils.unpack_ha_config import unpack_ha_config
