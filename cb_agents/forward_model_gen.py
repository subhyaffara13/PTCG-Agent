import random
from typing import Any

_ABILITY_DRAW = {"colress", "concealed", "flower selecting", "shining arcana"}

try:
    from cb_agents.card_registry import CardRegistry
except ImportError:
    CardRegistry = None


def _regenerate_legal_actions(gs: dict) -> None:
    if gs.get("turn_ended"):
        gs["legal_actions"] = []
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
            if CardRegistry is not None:
                try:
                    c = CardRegistry().get(int(card) if not isinstance(card, int) else card)
                    if c and getattr(c.card_type, "name", "") == "ENERGY":
                        if valid_targets:
                            for target in valid_targets:
                                if target: actions.append(f"attach_energy:{card}:{target}")
                        else:
                            actions.append(f"attach_energy:{card}")
                        continue
                    elif c and getattr(c.card_type, "name", "") == "TRAINER":
                        actions.append(f"play_trainer:{c.card_name}")
                        continue
                except Exception:
                    pass
            actions.append(f"attach_energy:{card}")
            actions.append(f"bench:{card}")
    bench = gs.get("my_bench", [])
    if isinstance(bench, list) and len(bench) > 0:
        for i in range(len(bench)):
            actions.append(f"retreat:{i}")
    opp_hp = gs.get("opponent_active_hp", 100)
    if opp_hp is not None and opp_hp > 0:
        actions.append("attack:strike")
    gs["legal_actions"] = list(dict.fromkeys(actions))


def _check_win_conditions(gs: dict) -> None:
    if gs.get("my_prizes", 6) <= 0:
        gs["game_over"] = True
        gs["winner"] = "me"
    elif gs.get("deck_out_loss", False) or gs.get("my_deck_count", 60) < 0:
        gs["game_over"] = True
        gs["winner"] = "opponent"
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
