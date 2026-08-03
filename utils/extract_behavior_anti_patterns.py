from typing import Any

def extract_behavior_anti_patterns(bv: Any, learned_donts: dict, save_donts_fn) -> bool:
    """Identifies bad behavioral thresholds."""
    changed = False
    if bv.setup_duration > 15:
        rule = {"condition": "setup_duration_gt_15", "description": "Strategy taking >15 turns to attack is a losing pattern."}
        if rule not in learned_donts["behavior_donts"]:
            learned_donts["behavior_donts"].append(rule)
            save_donts_fn()
            logger.info(f"Extracted behavior anti-pattern: {rule['description']}")
            changed = True
            
    if bv.energy_accel_rate < 0.2 and bv.turn_aggro > 0.5:
        rule = {"condition": "high_aggro_low_accel", "description": "Aggro profile without energy acceleration fails."}
        if rule not in learned_donts["behavior_donts"]:
            learned_donts["behavior_donts"].append(rule)
            save_donts_fn()
            logger.info(f"Extracted behavior anti-pattern: {rule['description']}")
            changed = True
    return changed

