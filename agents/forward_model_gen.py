import random
from typing import Any

try:
    from agents.card_registry import CardRegistry
except ImportError:
    CardRegistry = None


def _regenerate_legal_actions(gs: dict) -> None:
    if gs.get("turn_ended"):
        gs["legal_actions"] = []
        return
    actions = ["pass"]
    hand = gs.get("my_hand", [])
    if isinstance(hand, list) and len(hand) > 0:
        for card in hand:
            actions.append(f"attach_energy:{card}")
            actions.append(f"bench:{card}")
            if CardRegistry is not None:
                try:
                    c = CardRegistry().get(int(card) if not isinstance(card, int) else card)
                    if c and getattr(c.card_type, "name", "") == "TRAINER":
                        actions.append(f"play_trainer:{c.card_name}")
                except Exception:
                    pass
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
    hand = list(gs.get("my_hand", []))
    _remove_from_hand(hand, card_id)
    gs["my_hand"] = hand

    prev_stage_id = None
    if CardRegistry is not None:
        try:
            c = CardRegistry().get(int(card_id) if not isinstance(card_id, int) else card_id)
            if c and c.previous_stage:
                prev_stage_id = c.previous_stage
        except Exception:
            pass

    search_id = prev_stage_id if prev_stage_id is not None else card_id
    bench = list(gs.get("my_bench", []))
    for i, poke in enumerate(bench):
        if isinstance(poke, dict) and str(poke.get("id")) == str(search_id):
            bench[i] = {"id": f"evolved_{card_id}", "hp": 150, "attached": list(poke.get("attached", []))}
            gs["my_bench"] = bench
            return
    active = gs.get("my_active_pokemon", {})
    if isinstance(active, dict) and str(active.get("id")) == str(search_id):
        gs["my_active_pokemon"] = {"id": f"evolved_{card_id}", "hp": 150, "attached": list(active.get("attached", []))}
