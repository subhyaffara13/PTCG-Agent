import logging
from typing import List
from cb_agents.card_registry import CardRegistry
from cb_agents.card_types import CardStage

logger = logging.getLogger(__name__)
_registry = CardRegistry()

from cb_agents.constants import ABILITY_DRAW as _ABILITY_DRAW_KEYWORDS, SCALING_ATTACKERS

def _hand_strength(game_state: dict) -> str:
    hand = game_state.get("my_hand", [])
    hand_size = len(hand) if isinstance(hand, list) else 0
    if hand_size <= 2:
        return "weak"
    elif hand_size <= 4:
        return "medium"
    return "strong"

def _has_dead_weight(game_state: dict) -> bool:
    hand = game_state.get("my_hand", [])
    if not isinstance(hand, list) or len(hand) < 4:
        return False
    try:
        supporter_names = []
        basic_energy_count = 0
        stage2_count = 0
        search_count = 0
        deck_count = game_state.get("my_deck_count", 60)
        for cid_str in hand:
            try:
                card = _registry.get(int(cid_str))
                if card:
                    if card.card_type.name == "TRAINER" and getattr(card, "trainer_subtype", None) and card.trainer_subtype.name == "SUPPORTER":
                        supporter_names.append(card.card_name)
                    if card.card_type.name == "ENERGY":
                        basic_energy_count += 1
                    if card.stage and card.stage == CardStage.STAGE2:
                        stage2_count += 1
                    if card.card_type.name == "TRAINER" and getattr(card, "trainer_subtype", None) and card.trainer_subtype.name == "ITEM":
                        name_lower = card.card_name.lower()
                        if any(sk in name_lower for sk in ("ultra ball", "dusk ball", "pokegear", "energy search")):
                            search_count += 1
            except Exception as e:
                logger.debug(f"Dead weight card check failed for {cid_str}: {e}")
        dup_supporters = len(supporter_names) - len(set(supporter_names))
        score = 0
        if dup_supporters >= 2:
            score += dup_supporters
        if basic_energy_count >= 5:
            score += basic_energy_count - 4
        if stage2_count >= 2:
            score += stage2_count
        if search_count >= 2 and deck_count <= 20:
            score += search_count
        return score >= 4
    except Exception as e:
        logger.debug(f"Dead weight check execution failed: {e}")
        return False

def has_draw_remaining(candidates: List[str]) -> bool:
    for cand in candidates:
        try:
            if cand.startswith("play_trainer:"):
                name = cand.split(":", 1)[1].lower()
                if any(dk in name for dk in {"research", "iono", "judge", "concealed cards",
                                              "flower selecting", "shining arcana", "colress"}):
                    return True
            if cand.startswith("ability:"):
                target = cand.split(":", 1)[1].lower()
                if any(dk in target for dk in _ABILITY_DRAW_KEYWORDS):
                    return True
        except IndexError:
            continue
    return False

from cb_agents.heuristic_pipeline import _thinning_value, _pick_best_search, _dead_weight_heuristic, check_mcts_bypass
from cb_agents.turn_planner_sort import _has_evolution_target, sort_actions_heuristically, _EARLY_BENCH_ORDER
