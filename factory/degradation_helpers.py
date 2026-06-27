import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def evaluate_degradation_health(win_rate_history: List[float], diversity_history: List[float]) -> dict:
    """Helper to evaluate system health trends."""
    if len(win_rate_history) < 10:
        return {"is_degraded": False, "health_score": 1.0, "reasons": [], "suggested_action": "continue"}

    mid = len(win_rate_history) // 2
    old_wr = sum(win_rate_history[:mid]) / max(1, mid)
    new_wr = sum(win_rate_history[mid:]) / max(1, len(win_rate_history) - mid)
    
    old_div = sum(diversity_history[:mid]) / max(1, mid)
    new_div = sum(diversity_history[mid:]) / max(1, len(diversity_history) - mid)
    
    reasons = []
    is_degraded = False
    action = "continue"
    health_score = 1.0
    
    if new_wr < old_wr * 0.7:
        reasons.append(f"Catastrophic win rate collapse: {old_wr:.2f} -> {new_wr:.2f}")
        health_score -= 0.6
        is_degraded = True
        
    if new_div < 0.05 and old_div > 0.1:
        reasons.append("Policy mode collapse (diversity dropped near 0).")
        health_score -= 0.4
        is_degraded = True
        
    if is_degraded:
        if "win rate" in "".join(reasons).lower():
            action = "trigger_deck_optimizer"
        else:
            action = "trigger_strategy_optimizer"
            
    return {
        "is_degraded": is_degraded,
        "health_score": max(0.0, health_score),
        "reasons": reasons,
        "suggested_action": action
    }

def extract_healthy_behavior_patterns(iteration_result: Dict[str, Any], behavioral_vectors: Dict[str, Any], learned_dos: dict, save_dos_fn):
    """Extract behavior dos from successful iterations."""
    for label, game in iteration_result.get("games", {}).items():
        if game.get("winner") == "player_b":
            prizes_taken_b = game.get("prizes_taken_b", 0)
            turns = game.get("turns_taken", 999)
            
            if prizes_taken_b == 6 and turns < 12:
                logger.info("Extracting healthy pattern from overwhelming victory.")
                bv_b = behavioral_vectors.get("player_b")
                if bv_b and bv_b.energy_accel_rate > 1.0:
                    rule = {"condition": "high_accel_wins", "description": "Energy accel > 1.0 strongly correlates with fast wins."}
                    if rule not in learned_dos["behavior_dos"]:
                        learned_dos["behavior_dos"].append(rule)
                        save_dos_fn()
