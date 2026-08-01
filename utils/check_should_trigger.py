
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

