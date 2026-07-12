import random
from typing import Any
import logging

logger = logging.getLogger(__name__)

_ABILITY_DRAW = {"colress", "concealed", "flower selecting", "shining arcana"}

try:
    from cb_agents.card_registry import CardRegistry
except ImportError:
    CardRegistry = None


def _regenerate_legal_actions(gs: dict) -> None:
    if gs.get("turn_ended"):
        gs["legal_actions"] = []
        return
    
    # Prize selection phase: only take_prize actions are legal
    if gs.get("select_prize"):
        my_prizes = gs.get("my_prizes", [])
        if isinstance(my_prizes, list) and my_prizes:
            n = min(gs.get("prize_count", 1), len(my_prizes))
            actions = [f"take_prize:{i}" for i in range(n)]
        else:
            actions = [f"take_prize:{i}" for i in range(gs.get("prize_count", 1))]
        gs["legal_actions"] = actions
        return
    
    actions = ["pass"]
    hand = gs.get("my_hand", [])
    if isinstance(hand, list) and len(hand) > 0:
        valid_targets = []
        if isinstance(gs.get("my_active_pokemon"), dict) and gs.get("my_active_pokemon"):
            valid_targets.append(str(gs["my_active_pokemon"].get("id", "")))
        bench = gs.get("my_bench", [])
        if isinstance(bench, list):
            for p in bench:
                if isinstance(p, dict) and p.get("id"):
                    valid_targets.append(str(p["id"]))

        for card in hand:
            is_energy = False
            is_trainer = False
            if CardRegistry is not None:
                try:
                    c = CardRegistry().get(int(card) if not isinstance(card, int) else card)
                    if c:
                        ct = getattr(c.card_type, "name", "")
                        if ct == "ENERGY":
                            is_energy = True
                        elif ct == "TRAINER":
                            is_trainer = True
                except Exception as e:
                    logger.debug(f"Action prior generator: card {card} resolution failed: {e}")
            if is_energy:
                if valid_targets:
                    for target in valid_targets:
                        if target: actions.append(f"attach_energy:{card}:{target}")
                else:
                    actions.append(f"attach_energy:{card}")
                continue
            if is_trainer:
                actions.append(f"play_trainer:{c.card_name}")
                continue
            # Card is a Pokemon (or unknown): bench it, never attach_energy
            bench_list = gs.get("my_bench", [])
            if isinstance(bench_list, list) and len(bench_list) < 5:
                actions.append(f"bench:{card}")
            # Check if this card can evolve anything on the field
            if CardRegistry is not None and not is_energy and not is_trainer:
                try:
                    crd = CardRegistry().get(int(card) if not isinstance(card, int) else card)
                    if crd and crd.previous_stage:
                        prev_id = crd.previous_stage
                        prev_id_str = str(prev_id)
                        ap = gs.get("my_active_pokemon", {})
                        if isinstance(ap, dict) and str(ap.get("id", "")) == prev_id_str:
                            actions.append(f"evolve:{card}")
                        else:
                            for bp in gs.get("my_bench", []):
                                if isinstance(bp, dict) and str(bp.get("id", "")) == prev_id_str:
                                    actions.append(f"evolve:{card}")
                                    break
                except Exception:
                    pass
    bench = gs.get("my_bench", [])
    if isinstance(bench, list) and len(bench) > 0:
        for i in range(len(bench)):
            actions.append(f"retreat:{i}")
    opp_hp = gs.get("opponent_active_hp", 100)
    if opp_hp is not None and opp_hp > 0:
        my_active = gs.get("my_active_pokemon")
        can_attack = False
        if isinstance(my_active, dict):
            attached_count = len(my_active.get("attached", []))
            active_id = my_active.get("id")
            if active_id is not None and CardRegistry is not None:
                try:
                    min_cost = CardRegistry().get_min_energy_cost(active_id)
                    can_attack = attached_count >= min_cost
                except Exception:
                    can_attack = attached_count >= 1
            else:
                can_attack = attached_count >= 1
        else:
            can_attack = True
        if can_attack:
            actions.append("attack:strike")
    gs["legal_actions"] = list(dict.fromkeys(actions))


def _check_win_conditions(gs: dict) -> None:
    if gs.get("my_prizes", 6) <= 0:
        gs["game_over"] = True
        gs["winner"] = "me"
    elif gs.get("deck_out_loss", False) or gs.get("my_deck_count", 60) < 0:
        gs["game_over"] = True
        gs["winner"] = "opponent"
    elif gs.get("opponent_deck_out", False) or gs.get("opponent_deck_count", 60) < 0:
        gs["game_over"] = True
        gs["winner"] = "me"
    opp_hp = gs.get("opponent_active_hp", 100)
    opp_bench = gs.get("opponent_bench", [])
    if opp_hp <= 0 and not opp_bench:
        gs["game_over"] = True
        gs["winner"] = "me"


def _int_or_str(val: Any) -> Any:
    try:
        return int(val)
    except Exception:
        return val


def _remove_from_hand(hand: list, card_id: Any) -> None:
    try:
        hand.remove(card_id)
        return
    except (ValueError, TypeError):
        pass
    if isinstance(card_id, str):
        try:
            hand.remove(int(card_id))
            return
        except (ValueError, TypeError):
            pass


def _draw_cards(hand: list, gs: dict, n: int) -> list:
    dc = gs.get("my_deck_count", 60)
    drawn = min(n, dc)
    gs["my_deck_count"] = dc - drawn
    if n > dc:
        gs["deck_out_loss"] = True
    return hand + [0] * drawn


def _apply_evolve(gs: dict, card_id: Any) -> None:
    from cb_agents.forward_model_gen_helpers import apply_evolve_helper
    apply_evolve_helper(gs, card_id, CardRegistry, _remove_from_hand)
