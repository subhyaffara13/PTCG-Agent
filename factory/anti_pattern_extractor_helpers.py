import logging
from typing import List, Any
from cb_agents.card_registry import CardRegistry
from cb_agents.card_types import CardType

logger = logging.getLogger(__name__)

def extract_deck_anti_patterns(deck: List[int], learned_donts: dict, save_donts_fn) -> bool:
    """Identifies specific toxic combinations in a bad deck using LLM semantic analysis."""
    registry = CardRegistry()
    card_names = []
    energy_count = 0
    pokemon_count = 0
    trainer_count = 0
    
    for cid in deck:
        c = registry.get(cid)
        if not c: continue
        card_names.append(c.card_name)
        if c.card_type == CardType.ENERGY: energy_count += 1
        if c.card_type == CardType.POKEMON: pokemon_count += 1
        if c.card_type == CardType.TRAINER: trainer_count += 1

    # 1. Gemini LLM Deck Anti-Pattern Extraction
    import os
    import json
    import requests
    from collections import Counter
    from dotenv import load_dotenv
    
    load_dotenv()
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if gemini_key and card_names:
        counts = Counter(card_names)
        unique_cards_with_counts = [f"{name} (x{count})" for name, count in counts.items()]
        deck_str = "\n".join(unique_cards_with_counts)
        
        logger.info("AntiPatternExtractor: Requesting LLM deck analysis for anti-patterns...")
        prompt = f"""
        You are an expert Pokémon TCG Deck Analyst.
        We have identified a deck list that is performing exceptionally poorly (severe losses) on the leaderboard.
        
        Identify toxic ratios, dead-draw packages, element-type mismatch patterns, or sub-optimal card counts in this deck:
        
        ```
        {deck_str}
        ```
        
        Output a JSON object containing a list of `deck_donts` rules that specify what NOT to do based on this deck's flaws.
        """
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "deck_donts": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "condition": {"type": "STRING", "description": "A unique, short identifier slug for the anti-pattern (e.g. high_energy_no_draw)."},
                                    "description": {"type": "STRING", "description": "A clear, actionable warning description detailing why this deck ratio is poor."}
                                },
                                "required": ["condition", "description"]
                            }
                        }
                    },
                    "required": ["deck_donts"]
                }
            }
        }
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
            if res.status_code == 200:
                data = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(data)
                donts = parsed.get("deck_donts", [])
                
                changed = False
                for rule in donts:
                    if rule not in learned_donts["deck_donts"]:
                        learned_donts["deck_donts"].append(rule)
                        changed = True
                if changed:
                    save_donts_fn()
                    logger.info(f"Extracted {len(donts)} LLM-derived deck anti-patterns successfully.")
                    return True
        except Exception as e:
            logger.warning(f"LLM deck anti-pattern extraction failed: {e}. Falling back to baseline checker.")
        
    # 2. Baseline Checker Fallback
    changed = False
    if energy_count > 25 and trainer_count < 10:
        rule = {"condition": "energy_gt_25_trainer_lt_10", "description": "Deck has >25 energy but <10 trainers (dead draws)."}
        if rule not in learned_donts["deck_donts"]:
            learned_donts["deck_donts"].append(rule)
            save_donts_fn()
            logger.info(f"Extracted deck anti-pattern: {rule['description']}")
            changed = True
            
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
