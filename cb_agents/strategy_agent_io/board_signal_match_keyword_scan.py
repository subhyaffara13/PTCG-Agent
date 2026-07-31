from . import Any
from .flush_logs_load_skill_log_strategy import _opponent_archetype_signal

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

def keyword_scan(trigger_lower: str, profiles: dict[str, Any]) -> tuple[str | None, float]:
    best_key, best_score = None, 0.0
    for key, profile in profiles.items():
        trigger_desc = profile.get("trigger", "").lower()
        words = [w.strip("(),<>=") for w in trigger_desc.split() if len(w) > 3]
        if not words: continue
        matched = sum(1 for w in words if w in trigger_lower)
        score   = matched / len(words)
        if score > best_score:
            best_score, best_key = score, key
    return best_key, best_score

