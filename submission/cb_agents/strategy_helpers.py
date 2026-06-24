"""
agents/strategy_helpers.py

Helper logic for StrategyAgent: trigger evaluation and strategy selection rules.
"""

from typing import Dict, Any, List

def check_should_trigger(
    board_summary: Dict[str, Any],
    trigger: str,
    last_priority_profile: Any,
    strategy_thresholds: Dict[str, Any]
) -> tuple[bool, Dict[str, Any]]:
    # Read board state values safely
    my_prizes = board_summary.get("my_prizes_remaining", 6)
    opponent_prizes = board_summary.get("opponent_prizes_remaining", 6)
    opponent_confidence = board_summary.get("opponent_archetype_confidence", 0.0)
    priority_profile = board_summary.get("priority_profile", "aggro_push")
    turn_number = board_summary.get("turn_number", 1)
    
    prized_probabilities = board_summary.get("prized_probabilities", {})
    pikachu_prized_prob = prized_probabilities.get("721", 0.0)
    raichu_prized_prob = prized_probabilities.get("722", 0.0)

    sa_config = strategy_thresholds.get("strategy_agent", {}) if hasattr(strategy_thresholds, "get") else {}
    if not isinstance(sa_config, (dict, Any)) or not hasattr(sa_config, "get"):
        sa_config = {}
    trigger_rules = sa_config.get("trigger_rules", {})
    if not hasattr(trigger_rules, "get"):
        trigger_rules = {}

    prize_gap_threshold = int(trigger_rules.get("prize_gap_threshold", 2))
    opponent_confidence_threshold = float(trigger_rules.get("opponent_confidence_threshold", 0.75))
    raw_milestones = trigger_rules.get("turn_milestones", [3, 6, 9, 12, 15])
    turn_milestones = [int(x) for x in raw_milestones] if isinstance(raw_milestones, list) else [3, 6, 9, 12, 15]
    bench_count_min = int(trigger_rules.get("bench_count_min", 3))
    bench_opponent_prizes_min = int(trigger_rules.get("bench_opponent_prizes_min", 3))
    prized_attacker_threshold = float(trigger_rules.get("prized_attacker_threshold", 0.75))

    is_prize_gap = (my_prizes - opponent_prizes) >= prize_gap_threshold
    is_deck_identified = opponent_confidence > opponent_confidence_threshold
    is_hand_shift = (last_priority_profile is not None) and (priority_profile != last_priority_profile)
    is_explicit = trigger == "force_evaluate" or trigger == "prize_gap"
    is_turn_milestone = turn_number in turn_milestones
    my_bench_count = board_summary.get('my_bench_count', 0)
    is_bench_advantage = my_bench_count >= bench_count_min and opponent_prizes > bench_opponent_prizes_min
    is_prized_attacker = (pikachu_prized_prob >= prized_attacker_threshold or raichu_prized_prob >= prized_attacker_threshold)

    should_trigger = is_prize_gap or is_deck_identified or is_hand_shift or is_explicit or is_turn_milestone or is_bench_advantage or is_prized_attacker
    
    return should_trigger, sa_config

def select_new_strategy(
    board_summary: Dict[str, Any],
    active_strategy: str,
    sa_config: Dict[str, Any]
) -> str:
    my_prizes = board_summary.get("my_prizes_remaining", 6)
    opponent_prizes = board_summary.get("opponent_prizes_remaining", 6)
    opponent_archetype = board_summary.get("opponent_archetype", "unknown")
    bench_has_attacker = board_summary.get("bench_has_attacker", False)
    my_active_hp = board_summary.get("my_active_hp", 100)
    
    prized_probabilities = board_summary.get("prized_probabilities", {})
    pikachu_prized_prob = prized_probabilities.get("721", 0.0)
    raichu_prized_prob = prized_probabilities.get("722", 0.0)

    strat_selection = sa_config.get("strategy_selection", {}) if isinstance(sa_config, dict) else {}
    if not isinstance(strat_selection, dict):
        strat_selection = {}

    prized_attacker_extreme_threshold = float(strat_selection.get("prized_attacker_extreme_threshold", 0.99))
    prized_attacker_threshold = float(sa_config.get("trigger_rules", {}).get("prized_attacker_threshold", 0.75)) if isinstance(sa_config, dict) else 0.75
    opponent_prizes_low = int(strat_selection.get("opponent_prizes_low", 2))
    desperation_my_prizes_min = int(strat_selection.get("desperation_my_prizes_min", 5))
    desperation_opponent_prizes_max = int(strat_selection.get("desperation_opponent_prizes_max", 3))
    my_active_hp_critical = int(strat_selection.get("my_active_hp_critical", 30))

    is_prized_attacker = (pikachu_prized_prob >= prized_attacker_threshold or raichu_prized_prob >= prized_attacker_threshold)

    if pikachu_prized_prob >= prized_attacker_extreme_threshold or raichu_prized_prob >= prized_attacker_extreme_threshold:
        return 'stall'
    elif is_prized_attacker:
        return 'setup'
    elif opponent_prizes <= opponent_prizes_low:
        return 'closing'
    elif my_prizes >= desperation_my_prizes_min and opponent_prizes <= desperation_opponent_prizes_max:
        return 'aggro_push'
    elif opponent_archetype == 'aggro' and my_prizes < opponent_prizes:
        return 'stall'
    elif opponent_prizes <= opponent_prizes_low and my_prizes > opponent_prizes:
        return "aggro_push"
    elif my_active_hp < my_active_hp_critical and bench_has_attacker:
        return "setup"
    elif opponent_archetype == "control":
        return "disruption"

    return active_strategy
