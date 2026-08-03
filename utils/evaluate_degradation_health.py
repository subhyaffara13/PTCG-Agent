from typing import List

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

