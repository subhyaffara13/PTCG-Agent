from typing import Dict, Any

def unpack_ha_config(strategy_thresholds: Dict[str, Any]) -> dict:
    ha_config = strategy_thresholds.get("hand_analyst", {}) if hasattr(strategy_thresholds, "get") else {}
    if not hasattr(ha_config, "get"):
        ha_config = {}
    
    combo_mults = ha_config.get("combo_multipliers", {})
    penalties = ha_config.get("penalties", {})
    bonuses = ha_config.get("bonuses", {})
    profiles_config = ha_config.get("priority_profiles", {})
    
    return {
        "search_bench_mult": float(combo_mults.get("search_and_bench", 0.1)) if hasattr(combo_mults, "get") else 0.1,
        "discard_draw_mult": float(combo_mults.get("discard_and_draw", 0.15)) if hasattr(combo_mults, "get") else 0.15,
        "discard_search_energy_mult": float(combo_mults.get("discard_search_energy", 0.25)) if hasattr(combo_mults, "get") else 0.25,
        "rare_candy_stage2_mult": float(combo_mults.get("rare_candy_stage2", 0.35)) if hasattr(combo_mults, "get") else 0.35,
        "supp_thresh": int(penalties.get("supporter_oversaturation_threshold", 2)) if hasattr(penalties, "get") else 2,
        "supp_factor": float(penalties.get("supporter_oversaturation_factor", 0.1)) if hasattr(penalties, "get") else 0.1,
        "brick_factor": float(penalties.get("brick_factor", 0.15)) if hasattr(penalties, "get") else 0.15,
        "evo_match_factor": float(bonuses.get("evolution_match_factor", 0.20)) if hasattr(bonuses, "get") else 0.20,
        "early_basic_bonus": float(bonuses.get("early_basic", 0.15)) if hasattr(bonuses, "get") else 0.15,
        "early_supporter_bonus": float(bonuses.get("early_supporter", 0.1)) if hasattr(bonuses, "get") else 0.1,
        "mid_energy_bonus": float(bonuses.get("mid_energy", 0.15)) if hasattr(bonuses, "get") else 0.15,
        "mid_evolution_bonus": float(bonuses.get("mid_evolution", 0.1)) if hasattr(bonuses, "get") else 0.1,
        "late_attacker_bonus": float(bonuses.get("late_attacker", 0.15)) if hasattr(bonuses, "get") else 0.15,
        "late_high_ev_threshold": float(bonuses.get("late_high_ev_threshold", 0.6)) if hasattr(bonuses, "get") else 0.6,
        "late_high_ev_bonus": float(bonuses.get("late_high_ev_bonus", 0.1)) if hasattr(bonuses, "get") else 0.1,
        "closing_opp_prizes": int(profiles_config.get("closing", {}).get("opponent_prizes_max", 2)) if hasattr(profiles_config, "get") else 2,
        "aggro_push_hand_score": float(profiles_config.get("aggro_push", {}).get("hand_score_min", 0.35)) if hasattr(profiles_config, "get") else 0.35,
        "setup_hand_score": float(profiles_config.get("setup", {}).get("hand_score_max", 0.3)) if hasattr(profiles_config, "get") else 0.3,
        "disruption_control_count": int(profiles_config.get("disruption", {}).get("control_count_min", 2)) if hasattr(profiles_config, "get") else 2,
        "disruption_opp_prizes": int(profiles_config.get("disruption", {}).get("opponent_prizes_max", 3)) if hasattr(profiles_config, "get") else 3,
        "stall_deck_remaining": int(profiles_config.get("stall", {}).get("deck_remaining_max", 15)) if hasattr(profiles_config, "get") else 15,
    }
