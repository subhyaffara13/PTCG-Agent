"""
agents/action_masker_helpers.py

Helper logic for ActionMasker: masking illegal actions and calculating action signatures.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def mask_illegal_actions(legal_actions: List[str], game_state: dict) -> List[str]:
    """
    Remove truly invalid or nonsensical actions from the legal actions list.
    """
    if not legal_actions:
        return ["pass"]

    filtered = []
    my_bench = game_state.get("my_bench", [])
    my_hand = game_state.get("my_hand", [])
    my_deck_count = game_state.get("my_deck_count", 60)

    for action in legal_actions:
        if action.startswith("retreat:") and not my_bench:
            logger.debug(f"Masked {action}: no bench pokemon to retreat into")
            continue

        if action.startswith("attach_energy:") and not my_hand:
            logger.debug(f"Masked {action}: empty hand, no energy available")
            continue

        if action.startswith("play_trainer:") and my_deck_count <= 0:
            trainer_name = action.split(":", 1)[1].lower() if ":" in action else ""
            draw_keywords = ["research", "iono", "judge", "draw"]
            if any(k in trainer_name for k in draw_keywords):
                logger.debug(f"Masked {action}: would deck out (0 cards left)")
                continue

        filtered.append(action)

    if not filtered:
        return ["pass"]

    return filtered

def calculate_action_signature(action: str, bench_signatures: Dict[int, str], game_state: dict) -> str:
    """
    Compute a canonical signature for an action to detect isomorphisms.
    """
    parts = action.split(":")
    if len(parts) < 2:
        return action

    action_type = parts[0]
    target = parts[1]

    if target.startswith("bench_"):
        try:
            slot_idx = int(target.split("_")[1])
            if slot_idx in bench_signatures:
                return f"{action_type}:bench_sig_{bench_signatures[slot_idx]}"
        except (ValueError, IndexError):
            pass

    return action
