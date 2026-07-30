import logging
from typing import List, Dict, Any
logger = logging.getLogger(__name__)

def _compute_health_metrics(win_rate_history, diversity_history, mid):
    old_wr = sum(win_rate_history[:mid]) / max(1, mid)
    new_wr = sum(win_rate_history[mid:]) / max(1, len(win_rate_history) - mid)
    old_div = sum(diversity_history[:mid]) / max(1, mid)
    new_div = sum(diversity_history[mid:]) / max(1, len(diversity_history) - mid)
    return old_wr, new_wr, old_div, new_div

def _decide_action(reasons):
    joined = "".join(reasons).lower()
    return "trigger_deck_optimizer" if "win rate" in joined else "trigger_strategy_optimizer"

def _extract_healthy_pattern(iteration_result, behavioral_vectors, learned_dos, save_dos_fn):
    import logging
    logger = logging.getLogger(__name__)
    for label, game in iteration_result.get("games", {}).items():
        if game.get("winner") != "player_b": continue
        prizes_taken_b, turns = game.get("prizes_taken_b", 0), game.get("turns_taken", 999)
        if prizes_taken_b < 4 or turns >= 16: continue
        logger.info("Extracting healthy pattern from overwhelming victory.")
        bv_b = behavioral_vectors.get("player_b")
        if bv_b and bv_b.energy_accel_rate > 0.5:
            rule = {"condition": "high_accel_wins", "description": "Energy accel > 0.5 strongly correlates with fast wins."}
            modified = False
            for key in ("behavior_dos", "setup_profiles"):
                if key not in learned_dos: learned_dos[key] = []
                if rule not in learned_dos[key]:
                    learned_dos[key].append(rule); modified = True
            if modified: save_dos_fn()
