
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

    val_extreme = merged_sel.get("prized_attacker_extreme_threshold", 0.7)
    prized_attacker_extreme_threshold = float(val_extreme) if isinstance(val_extreme, (int, float, str)) else 0.7

    val_thresh = merged_trigger_s.get("prized_attacker_threshold", 0.5)
    prized_attacker_threshold = float(val_thresh) if isinstance(val_thresh, (int, float, str)) else 0.5

    opponent_prizes_low = int(merged_sel.get("opponent_prizes_low", 2))
    desperation_my_prizes_min = int(merged_sel.get("desperation_my_prizes_min", 4))
    desperation_opponent_prizes_max = int(merged_sel.get("desperation_opponent_prizes_max", 2))
    my_active_hp_critical = int(merged_sel.get("my_active_hp_critical", 30))

    raw_deck = board_summary.get("my_decklist") or board_summary.get("decklist")
    decklist = raw_deck if isinstance(raw_deck, dict) else {}
    p_probs = prized_pokemon_probs(state.prized_probabilities, decklist)
    is_prized_attacker = any(prob >= prized_attacker_threshold for prob in p_probs)
    is_prized_attacker_extreme = any(prob >= prized_attacker_extreme_threshold for prob in p_probs)

    if state.my_prizes_remaining <= 2:
        return 'closing'
    elif is_prized_attacker_extreme:
        return 'stall'
    elif is_prized_attacker:
        return 'setup'
    elif state.opponent_prizes_remaining <= opponent_prizes_low:
        if state.my_prizes_remaining <= state.opponent_prizes_remaining:
            return "aggro_push"
        return "control"
    elif state.my_prizes_remaining <= state.opponent_prizes_remaining:
        return 'aggro_push'
    elif state.opponent_archetype == 'aggro' and state.my_prizes_remaining > state.opponent_prizes_remaining:
        return 'stall'
    elif state.my_active_hp < my_active_hp_critical and state.bench_has_attacker:
        return "setup"
    elif state.opponent_archetype == "control":
        return "control"

    return active_strategy


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

    val_extreme = merged_sel.get("prized_attacker_extreme_threshold", 0.7)
    prized_attacker_extreme_threshold = float(val_extreme) if isinstance(val_extreme, (int, float, str)) else 0.7

    val_thresh = merged_trigger_s.get("prized_attacker_threshold", 0.5)
    prized_attacker_threshold = float(val_thresh) if isinstance(val_thresh, (int, float, str)) else 0.5

    opponent_prizes_low = int(merged_sel.get("opponent_prizes_low", 2))
    desperation_my_prizes_min = int(merged_sel.get("desperation_my_prizes_min", 4))
    desperation_opponent_prizes_max = int(merged_sel.get("desperation_opponent_prizes_max", 2))
    my_active_hp_critical = int(merged_sel.get("my_active_hp_critical", 30))

    raw_deck = board_summary.get("my_decklist") or board_summary.get("decklist")
    decklist = raw_deck if isinstance(raw_deck, dict) else {}
    p_probs = prized_pokemon_probs(state.prized_probabilities, decklist)
    is_prized_attacker = any(prob >= prized_attacker_threshold for prob in p_probs)
    is_prized_attacker_extreme = any(prob >= prized_attacker_extreme_threshold for prob in p_probs)

    if state.my_prizes_remaining <= 2:
        return 'closing'
    elif is_prized_attacker_extreme:
        return 'stall'
    elif is_prized_attacker:
        return 'setup'
    elif state.opponent_prizes_remaining <= opponent_prizes_low:
        if state.my_prizes_remaining <= state.opponent_prizes_remaining:
            return "aggro_push"
        return "control"
    elif state.my_prizes_remaining <= state.opponent_prizes_remaining:
        return 'aggro_push'
    elif state.opponent_archetype == 'aggro' and state.my_prizes_remaining > state.opponent_prizes_remaining:
        return 'stall'
    elif state.my_active_hp < my_active_hp_critical and state.bench_has_attacker:
        return "setup"
    elif state.opponent_archetype == "control":
        return "control"

    return active_strategy


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
        return "disruption"
    elif state.my_prizes_remaining >= desperation_my_prizes_min and state.opponent_prizes_remaining <= desperation_opponent_prizes_max:
        return 'aggro_push'
    elif state.opponent_archetype == 'aggro' and state.my_prizes_remaining < state.opponent_prizes_remaining:
        return 'stall'
    elif state.my_active_hp < my_active_hp_critical and state.bench_has_attacker:
        return "setup"
    elif state.opponent_archetype == "control":
        return "disruption"

    return active_strategy

