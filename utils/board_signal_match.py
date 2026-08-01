
def board_signal_match(board_summary: dict[str, Any]) -> str | None:
    prizes     = board_summary.get("prizes")
    if prizes is None: prizes = board_summary.get("my_prizes_remaining")
    bench      = board_summary.get("bench_count")
    if bench is None: bench = board_summary.get("my_bench_count")
    score      = board_summary.get("hand_score")
    energy     = board_summary.get("energy_attached")
    opp_prizes = board_summary.get("opponent_prizes")
    if opp_prizes is None: opp_prizes = board_summary.get("opponent_prizes_remaining")
    boss_prob  = board_summary.get("boss_prob", 0.0)
    iono_prob  = board_summary.get("iono_prob", 0.0)
    path_prob  = board_summary.get("path_prob", 0.0)
    hammer_prob = board_summary.get("hammer_prob", 0.0)

    # Opponent archetype overrides
    arch_sig = _opponent_archetype_signal(board_summary)
    if arch_sig is not None:
        return arch_sig

    # Disruption awareness (softer thresholds than before)
    if boss_prob > 0.6 and bench is not None and int(bench) > 0: return "stall"
    if iono_prob > 0.6 and score is not None and float(score) > 5.0: return "aggro_push"
    if path_prob > 0.5: return "setup"  # Path blocks abilities — need to find stadium answer
    if hammer_prob > 0.6: return "energy_stall"  # Energy removal risk — attach conservatively
    if prizes is not None and int(prizes) <= 2: return "endgame_close"
    if opp_prizes is not None and int(opp_prizes) <= 2: return "prize_race"
    if bench is not None and int(bench) <= 1: return "bench_low"
    if energy is not None and int(energy) == 0:
        turn_num = board_summary.get("turn_number", 1)
        if turn_num > 2:
            return "energy_stall"
    if score is not None and float(score) < 2.0: return "hand_dead"
        
    p_val = int(prizes) if prizes is not None else 6
    if p_val >= 5: return "setup"
    if p_val >= 3: return "aggro"
    return "endgame_close"


def board_signal_match(board_summary: dict[str, Any]) -> str | None:
    prizes     = board_summary.get("prizes")
    if prizes is None: prizes = board_summary.get("my_prizes_remaining")
    bench      = board_summary.get("bench_count")
    if bench is None: bench = board_summary.get("my_bench_count")
    score      = board_summary.get("hand_score")
    energy     = board_summary.get("energy_attached")
    opp_prizes = board_summary.get("opponent_prizes")
    if opp_prizes is None: opp_prizes = board_summary.get("opponent_prizes_remaining")
    boss_prob  = board_summary.get("boss_prob", 0.0)
    iono_prob  = board_summary.get("iono_prob", 0.0)

    if boss_prob > 0.7 and bench is not None and int(bench) > 0: return "stall"
    if iono_prob > 0.7 and score is not None and float(score) > 5.0: return "aggro_push"
    if prizes is not None and int(prizes) <= 2: return "endgame_close"
    if opp_prizes is not None and int(opp_prizes) <= 2: return "prize_race"
    if bench is not None and int(bench) <= 1: return "bench_low"
    if energy is not None and int(energy) == 0: return "energy_stall"
    if score is not None and float(score) < 2.0: return "hand_dead"
        
    p_val = int(prizes) if prizes is not None else 6
    if p_val >= 5: return "setup"
    if p_val >= 3: return "aggro"
    return "endgame_close"


def board_signal_match(board_summary: dict[str, Any]) -> str | None:
    prizes     = board_summary.get("prizes")
    if prizes is None: prizes = board_summary.get("my_prizes_remaining")
    bench      = board_summary.get("bench_count")
    if bench is None: bench = board_summary.get("my_bench_count")
    score      = board_summary.get("hand_score")
    energy     = board_summary.get("energy_attached")
    opp_prizes = board_summary.get("opponent_prizes")
    if opp_prizes is None: opp_prizes = board_summary.get("opponent_prizes_remaining")
    boss_prob  = board_summary.get("boss_prob", 0.0)
    iono_prob  = board_summary.get("iono_prob", 0.0)
    path_prob  = board_summary.get("path_prob", 0.0)
    hammer_prob = board_summary.get("hammer_prob", 0.0)

    # Opponent archetype overrides
    arch_sig = _opponent_archetype_signal(board_summary)
    if arch_sig is not None:
        return arch_sig

    # Disruption awareness (softer thresholds than before)
    if boss_prob > 0.6 and bench is not None and int(bench) > 0: return "stall"
    if iono_prob > 0.6 and score is not None and float(score) > 5.0: return "aggro_push"
    if path_prob > 0.5: return "setup"  # Path blocks abilities — need to find stadium answer
    if hammer_prob > 0.6: return "energy_stall"  # Energy removal risk — attach conservatively
    if prizes is not None and int(prizes) <= 2: return "endgame_close"
    if opp_prizes is not None and int(opp_prizes) <= 2: return "prize_race"
    if bench is not None and int(bench) <= 1: return "bench_low"
    if energy is not None and int(energy) == 0:
        turn_num = board_summary.get("turn_number", 1)
        if turn_num > 2:
            return "energy_stall"
    if score is not None and float(score) < 2.0: return "hand_dead"
        
    p_val = int(prizes) if prizes is not None else 6
    if p_val >= 5: return "setup"
    if p_val >= 3: return "aggro"
    return "endgame_close"

