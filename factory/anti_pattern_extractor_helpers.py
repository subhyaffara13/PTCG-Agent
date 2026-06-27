import logging
from typing import List, Any
from agents.card_registry import CardRegistry
from agents.card_types import CardType

logger = logging.getLogger(__name__)

def extract_deck_anti_patterns(deck: List[int], learned_donts: dict, save_donts_fn) -> bool:
    """Identifies specific toxic combinations in a bad deck."""
    registry = CardRegistry()
    energy_count = 0
    pokemon_count = 0
    trainer_count = 0
    
    for cid in deck:
        c = registry.get(cid)
        if not c: continue
        if c.card_type == CardType.ENERGY: energy_count += 1
        if c.card_type == CardType.POKEMON: pokemon_count += 1
        if c.card_type == CardType.TRAINER: trainer_count += 1
        
    changed = False
    # Example Don't: Too much energy, no trainers
    if energy_count > 25 and trainer_count < 10:
        rule = {"condition": "energy_gt_25_trainer_lt_10", "description": "Deck has >25 energy but <10 trainers (dead draws)."}
        if rule not in learned_donts["deck_donts"]:
            learned_donts["deck_donts"].append(rule)
            save_donts_fn()
            logger.info(f"Extracted deck anti-pattern: {rule['description']}")
            changed = True
            
    # Example Don't: Too many pokemon
    if pokemon_count > 30:
        rule = {"condition": "pokemon_gt_30", "description": "Deck has >30 pokemon, clogs hand."}
        if rule not in learned_donts["deck_donts"]:
            learned_donts["deck_donts"].append(rule)
            save_donts_fn()
            logger.info(f"Extracted deck anti-pattern: {rule['description']}")
            changed = True
    return changed

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
