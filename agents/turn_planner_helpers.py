import logging

from agents.prize_tracker import PrizeTracker
from agents.heuristic_pipeline import pipeline

logger = logging.getLogger(__name__)


def _process_prize_tracker(game_state: dict, prize_tracker: PrizeTracker, packet) -> dict:
    initial_decklist = game_state.get("my_decklist", {})
    if initial_decklist and not prize_tracker.initial_decklist:
        prize_tracker.record_initial_decklist(initial_decklist)
    hand_ids = game_state.get("my_hand", [])
    if isinstance(hand_ids, list) and hand_ids and prize_tracker.initial_decklist:
        is_search = game_state.get("is_searching", False) or (isinstance(game_state.get("my_deck", []), list) and len(game_state.get("my_deck", [])) > 0)
        if is_search:
            discard_ids = game_state.get("my_discard", [])
            board_ids = list(game_state.get("my_board", []))
            active = game_state.get("my_active_pokemon", {})
            if isinstance(active, dict):
                aid = active.get("id")
                if aid is not None:
                    board_ids.append(int(aid) if not isinstance(aid, int) else aid)
                for att in active.get("attached", []):
                    try: board_ids.append(int(att))
                    except: pass
            for poke in game_state.get("my_bench", []):
                if isinstance(poke, dict):
                    pid = poke.get("id")
                    if pid is not None:
                        board_ids.append(int(pid) if not isinstance(pid, int) else pid)
                    for att in poke.get("attached", []):
                        try: board_ids.append(int(att))
                        except: pass
            deck_contents = game_state.get("my_deck", [])
            deck_remaining = game_state.get("my_deck_count", 0)
            prize_tracker.on_deck_search(hand_ids, discard_ids, board_ids, deck_contents, deck_remaining)
    prized_enrich = prize_tracker.get_certainty_enrichment()
    if prized_enrich:
        game_state.update(prized_enrich)
        prized_card_types = len(prized_enrich.get('prized_card_ids', {}))
        logger.debug(f"Injected prized certainty into game_state: {prized_card_types} card types")
    return game_state


def _check_lethal_and_update(game_state: dict) -> None:
    from agents.card_registry import CardRegistry
    registry = CardRegistry()
    legal_attacks = game_state.get("legal_attacks", [])
    max_damage = 0
    for att in legal_attacks:
        try:
            card = registry.get_full_skill(att)
            if card and card.damage_output > max_damage:
                max_damage = card.damage_output
        except:
            pass

    lethal = pipeline.check_lethal(
        my_damage=max_damage,
        opp_hp=game_state.get("opponent_active_hp", 100),
        legal_attacks=legal_attacks,
        opp_active_id=game_state.get("opponent_active", {}).get("id") if isinstance(game_state.get("opponent_active"), dict) else game_state.get("opponent_active"),
        my_hp=game_state.get("my_active_hp", 100),
        legal_retreats=game_state.get("legal_retreats", []),
        my_attached=len(game_state.get("my_active_pokemon", {}).get("attached", [])) if isinstance(game_state.get("my_active_pokemon"), dict) else 0,
    )
    if lethal.get("action_override"):
        game_state["lethal_action_override"] = lethal["action_override"]
    if lethal.get("retreat_score_boost"):
        game_state["retreat_score_boost"] = lethal["retreat_score_boost"]
        game_state["retreat_target"] = lethal.get("retreat_target")
