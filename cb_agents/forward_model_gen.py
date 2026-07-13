import random
import json
from pathlib import Path
from typing import Any
import logging

logger = logging.getLogger(__name__)

from cb_agents.card_utils import _get_prize_yield, _int_or_str
from cb_agents.constants import ABILITY_DRAW as _ABILITY_DRAW

try:
    from cb_agents.card_registry import CardRegistry
except ImportError:
    CardRegistry = None


def _count_high_prize_on_board(gs: dict) -> int:
    """Count how many high-prize (prize_yield>=2) Pokemon are on our board."""
    count = 0
    active = gs.get("my_active_pokemon", {})
    if isinstance(active, dict):
        if _get_prize_yield(str(active.get("card_name", ""))) >= 2:
            count += 1
    for bp in gs.get("my_bench", []):
        if isinstance(bp, dict):
            if _get_prize_yield(str(bp.get("card_name", ""))) >= 2:
                count += 1
    return count

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
                # Enforce one Supporter per turn in MCTS rollouts
                _skip = False
                if gs.get("supporter_played_this_turn"):
                    try:
                        _fc = CardRegistry().get_full_skill(int(card) if not isinstance(card, int) else card)
                        if _fc and getattr(_fc, 'trainer_subtype', None) and _fc.trainer_subtype.name == "SUPPORTER":
                            _skip = True
                    except Exception:
                        pass
                if not _skip:
                    actions.append(f"play_trainer:{c.card_name}")
                continue
            # Boss-aware bench protection: skip benching high-prize if opponent has Boss and we already expose one
            _skip_bench = False
            if CardRegistry is not None:
                try:
                    _cc = CardRegistry().get(int(card) if not isinstance(card, int) else card)
                    if _cc and _get_prize_yield(_cc.card_name) >= 2:
                        _boss_p = gs.get("boss_prob", 0.0)
                        if _boss_p > 0.3 and _count_high_prize_on_board(gs) >= 1:
                            _skip_bench = True
                except Exception:
                    pass
            # Card is a Pokemon (or unknown): bench it, never attach_energy
            bench_list = gs.get("my_bench", [])
            if isinstance(bench_list, list) and len(bench_list) < 5 and not _skip_bench:
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


def _load_concede_thresholds() -> dict:
    thresholds = {
        "prize_gap_min": 3,
        "deck_out_max": 2,
        "prevent_prize_gap": 3,
    }
    try:
        result_path = next(
            (Path(p) / "iteration_result.json" for p in ["logs", "data", "."] if (Path(p) / "iteration_result.json").exists()),
            None
        )
        if result_path and result_path.exists():
            data = json.loads(result_path.read_text(encoding="utf-8"))
            games = data.get("games", {})
            deck_games = [g for k, g in games.items() if k.startswith("deck_test")]
            if len(deck_games) >= 10:
                wins = sum(1 for g in deck_games if g.get("winner") == "player_b")
                wr = wins / len(deck_games)
                if wr < 0.3:
                    thresholds["prize_gap_min"] = 2
                    thresholds["deck_out_max"] = 3
                elif wr > 0.7:
                    thresholds["prize_gap_min"] = 4
    except Exception:
        pass
    return thresholds


def _check_concede(gs: dict) -> bool:
    _concede_thresholds = _load_concede_thresholds()
    prize_gap_min = _concede_thresholds["prize_gap_min"]
    deck_out_max = _concede_thresholds["deck_out_max"]
    prevent_prize_gap = _concede_thresholds["prevent_prize_gap"]
    my_prizes = gs.get("my_prizes", 6)
    opp_prizes = gs.get("opponent_prizes", 6)
    my_bench = gs.get("my_bench", [])
    my_hp = gs.get("my_active_hp", 100) if gs.get("my_active_pokemon") else 0
    my_deck = gs.get("my_deck_count", 60)

    # No Pokemon left on board
    if my_hp <= 0 and not my_bench:
        return True

    # Opponent has taken almost all prizes; we have taken none
    if my_prizes <= 0 and opp_prizes >= prize_gap_min:
        return True

    # Deck-out imminent with no realistic comeback (we need multiple KOs, opponent needs 0)
    if my_deck <= deck_out_max and opp_prizes >= prize_gap_min and my_prizes >= prevent_prize_gap:
        return True

    # Opponent about to take last prize and we can't prevent it
    if opp_prizes <= 1 and my_prizes >= prevent_prize_gap:
        opp_hp = gs.get("opponent_active_hp", 100)
        if opp_hp > 0:
            return True

    return False


def _check_win_conditions(gs: dict) -> None:
    if gs.get("my_prizes", 6) <= 0:
        gs["game_over"] = True
        gs["winner"] = "me"
        return
    if gs.get("opponent_prizes", 6) <= 0:
        gs["game_over"] = True
        gs["winner"] = "opponent"
        return
    if gs.get("deck_out_loss", False) or gs.get("my_deck_count", 60) < 0:
        gs["game_over"] = True
        gs["winner"] = "opponent"
        return
    if gs.get("opponent_deck_out", False) or gs.get("opponent_deck_count", 60) < 0:
        gs["game_over"] = True
        gs["winner"] = "me"
        return
    my_hp = gs.get("my_active_hp", 100) if gs.get("my_active_pokemon") else 0
    my_bench = gs.get("my_bench", [])
    if my_hp <= 0 and not my_bench:
        gs["game_over"] = True
        gs["winner"] = "opponent"
        return
    opp_hp = gs.get("opponent_active_hp", 100)
    opp_bench = gs.get("opponent_bench", [])
    if opp_hp <= 0 and not opp_bench:
        gs["game_over"] = True
        gs["winner"] = "me"
        return

    # Hopeless position check — concede to save simulation time
    if _check_concede(gs):
        gs["game_over"] = True
        gs["winner"] = "opponent"
        gs["conceded"] = True


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
