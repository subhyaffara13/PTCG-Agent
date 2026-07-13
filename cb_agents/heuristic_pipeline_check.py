"""
Sub-module: check_lethal, mask_illegal, _calc_sig
"""

import logging
from typing import Dict, List
from cb_agents.card_registry import CardRegistry

logger = logging.getLogger(__name__)
_registry = CardRegistry()


def _get_prize_yield(card_name: str) -> int:
    if not card_name:
        return 1
    n = card_name.lower()
    if "vmax" in n:
        return 3
    if "vstar" in n or n.endswith(" v") or n.endswith(" ex") or " ex " in n or " v " in n:
        return 2
    return 1


def check_lethal(my_damage: int, opp_hp: int, legal_attacks: list,
                 opp_active_id, my_hp: int, legal_retreats: list,
                 my_attached: int = 0, boss_prob: float = 0.0) -> dict:
    if legal_attacks and my_damage >= opp_hp and my_damage > 0:
        import re
        best_attack = None
        for attack in legal_attacks:
            move_name = str(attack).replace("attack:", "").strip().lower()
            dmg_str = _registry.move_damage.get(move_name, "0")
            dmg_val = 0
            try:
                match = re.match(r"^(\d+)", dmg_str)
                if match:
                    dmg_val = int(match.group(1))
            except Exception:
                pass
            if dmg_val >= opp_hp:
                best_attack = attack
                break
        if best_attack is None:
            best_attack = legal_attacks[0]
        reasoning = f"Lethal: my_damage {my_damage} >= opp_hp {opp_hp}"
        best_attack_name = str(best_attack).replace("attack:", "")
        return {"action_override": f"attack:{best_attack_name}", "reasoning_chain": reasoning}
    if opp_active_id is not None:
        try:
            from cb_agents.card_registry import CardRegistry
            opp_card = CardRegistry().get_full_skill(opp_active_id)
            if opp_card and opp_card.damage_output >= my_hp and opp_card.damage_output > 0:
                if legal_retreats:
                    can_counter = my_damage >= opp_hp and my_attached > 0
                    if not can_counter:
                        # Don't force retreat if opponent likely has Boss's Orders
                        # (they'll just drag back the retreat target or something worse)
                        if boss_prob > 0.5:
                            reasoning = f"Opponent lethal threat but boss_prob={boss_prob:.2f}. Retreat may be wasted (Boss's back). Skip boost."
                            return {"action_override": None, "reasoning_chain": reasoning}
                        tgt = legal_retreats[0]
                        reasoning = f"Opponent lethal threat (damage {opp_card.damage_output} >= HP {my_hp}). Boost retreat:{tgt} +1.0"
                        return {"action_override": None, "retreat_score_boost": 1.0, "retreat_target": tgt, "reasoning_chain": reasoning}
        except Exception as e:
            logger.error(f"check_lethal registry error: {e}")
    return {"action_override": None, "reasoning_chain": "No lethal found."}


def mask_illegal(legal_actions: list, game_state: dict) -> list:
    if not legal_actions: return ["pass"]
    filtered = []
    my_bench = game_state.get("my_bench", [])
    my_hand = game_state.get("my_hand", [])
    my_deck_count = game_state.get("my_deck_count", 60)
    for action in legal_actions:
        if action.startswith("retreat:") and not my_bench: continue
        # Removed aggressive stripping of attach_energy so the bot can attach energy
        if action.startswith("play_trainer:") and my_deck_count <= 0:
            trainer_name = action.split(":", 1)[1].lower() if ":" in action else ""
            if any(k in trainer_name for k in ["research", "iono", "judge", "draw"]): continue
        filtered.append(action)
    return filtered or ["pass"]


def _calc_sig(action: str, bench_sigs: Dict[int, str], gs: dict) -> str:
    parts = action.split(":")
    if len(parts) < 2:
        return action
    target = parts[1]
    if target.startswith("bench_"):
        try:
            idx = int(target.split("_")[1])
            if idx in bench_sigs:
                return f"{parts[0]}:bench_sig_{bench_sigs[idx]}"
        except (ValueError, IndexError):
            pass
    return action
