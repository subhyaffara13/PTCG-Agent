"""
cb_agents/strategy_helpers.py

Helper logic for StrategyAgent: trigger evaluation and strategy selection rules.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from cb_agents.configs import DEFAULT_TRIGGER_RULES, DEFAULT_STRATEGY_SELECTION
from cb_agents.board_state import BoardState
from cb_agents.prized_helpers import prized_pokemon_probs


def check_should_trigger(
    board_summary: Dict[str, Any],
    trigger: str,
    last_priority_profile: Any,
    strategy_thresholds: Dict[str, Any]
) -> tuple[bool, Dict[str, Any]]:
    state = BoardState.from_dict(board_summary)

    sa_config = strategy_thresholds.get("strategy_agent", {}) if hasattr(strategy_thresholds, "get") else {}
    if not isinstance(sa_config, dict) or not hasattr(sa_config, "get"):
        sa_config = {}
    trigger_rules = sa_config.get("trigger_rules", {})
    if not isinstance(trigger_rules, dict):
        trigger_rules = {}
    merged = {**DEFAULT_TRIGGER_RULES, **trigger_rules}

    prize_gap_threshold = int(merged["prize_gap_threshold"])
    opponent_confidence_threshold = float(merged["opponent_confidence_threshold"])
    raw_milestones = merged["turn_milestones"]
    turn_milestones = [int(x) for x in raw_milestones] if isinstance(raw_milestones, list) else DEFAULT_TRIGGER_RULES["turn_milestones"]
    bench_count_min = int(merged["bench_count_min"])
    bench_opponent_prizes_min = int(merged["bench_opponent_prizes_min"])
    prized_attacker_threshold = float(merged["prized_attacker_threshold"])

    is_prize_gap = (state.my_prizes_remaining - state.opponent_prizes_remaining) >= prize_gap_threshold
    is_deck_identified = state.opponent_archetype_confidence > opponent_confidence_threshold
    is_hand_shift = (last_priority_profile is not None) and (state.priority_profile != last_priority_profile)
    is_explicit = trigger == "force_evaluate" or trigger == "prize_gap"
    is_turn_milestone = state.turn_number in turn_milestones
    is_bench_advantage = state.my_bench_count >= bench_count_min and state.opponent_prizes_remaining > bench_opponent_prizes_min
    
    decklist = board_summary.get("my_decklist", board_summary.get("decklist", {}))
    p_probs = prized_pokemon_probs(state.prized_probabilities, decklist)
    is_prized_attacker = any(prob >= prized_attacker_threshold for prob in p_probs)

    should_trigger = is_prize_gap or is_deck_identified or is_hand_shift or is_explicit or is_turn_milestone or is_bench_advantage or is_prized_attacker
    
    return should_trigger, sa_config

def select_new_strategy(
    board_summary: Dict[str, Any],
    active_strategy: str,
    sa_config: Dict[str, Any]
) -> str:
    state = BoardState.from_dict(board_summary)

    strat_selection = sa_config.get("strategy_selection", {}) if isinstance(sa_config, dict) else {}
    if not isinstance(strat_selection, dict):
        strat_selection = {}
    merged_sel = {**DEFAULT_STRATEGY_SELECTION, **strat_selection}
    trigger_rules_s = sa_config.get("trigger_rules", {}) if isinstance(sa_config, dict) else {}
    merged_trigger_s = {**DEFAULT_TRIGGER_RULES, **(trigger_rules_s if isinstance(trigger_rules_s, dict) else {})}

    prized_attacker_extreme_threshold = float(merged_sel["prized_attacker_extreme_threshold"])
    prized_attacker_threshold = float(merged_trigger_s["prized_attacker_threshold"])
    opponent_prizes_low = int(merged_sel["opponent_prizes_low"])
    desperation_my_prizes_min = int(merged_sel["desperation_my_prizes_min"])
    desperation_opponent_prizes_max = int(merged_sel["desperation_opponent_prizes_max"])
    my_active_hp_critical = int(merged_sel["my_active_hp_critical"])

    decklist = board_summary.get("my_decklist", board_summary.get("decklist", {}))
    p_probs = prized_pokemon_probs(state.prized_probabilities, decklist)
    is_prized_attacker = any(prob >= prized_attacker_threshold for prob in p_probs)
    is_prized_attacker_extreme = any(prob >= prized_attacker_extreme_threshold for prob in p_probs)

    if is_prized_attacker_extreme:
        return 'stall'
    elif is_prized_attacker:
        return 'setup'
    elif state.opponent_prizes_remaining <= opponent_prizes_low:
        if state.my_prizes_remaining > state.opponent_prizes_remaining:
            return "aggro_push"
        return "control"
    elif state.my_prizes_remaining >= desperation_my_prizes_min and state.opponent_prizes_remaining <= desperation_opponent_prizes_max:
        return 'aggro_push'
    elif state.opponent_archetype == 'aggro' and state.my_prizes_remaining < state.opponent_prizes_remaining:
        return 'stall'
    elif state.my_active_hp < my_active_hp_critical and state.bench_has_attacker:
        return "setup"
    elif state.opponent_archetype == "control":
        return "control"

    return active_strategy
