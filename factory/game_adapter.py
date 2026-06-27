import logging
from pathlib import Path
from factory.game_adapter_helpers import get_mapped_indices

logger = logging.getLogger(__name__)

def run_agent_turn(orchestrator, observation: dict, deck: list[int]) -> list[int]:
    """Interactions adapter mapping CABT observations to Orchestrator and actions back to options."""
    select = observation.get("select")
    if select is None: return deck

    options = select.get("option", [])
    max_count = select.get("maxCount", 1)
    fallback_action = list(range(min(max_count, len(options))))

    try:
        current = observation.get("current")
        if not current: return fallback_action

        my_idx = current.get("yourIndex", 0)
        players = current.get("players", [])
        if len(players) <= my_idx: return fallback_action

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}

        def _get_id(c):
            if hasattr(c, "id"): return getattr(c, "id")
            if isinstance(c, dict): return c.get("id") or c.get("cardId") or c.get("name")
            return None

        my_board_ids = []
        for zone in ["active", "bench"]:
            if my_state.get(zone):
                for c in my_state[zone]:
                    _id = _get_id(c)
                    if _id is not None: my_board_ids.append(_id)

        my_active_damage = 0
        if my_state.get("active") and len(my_state["active"]) > 0:
            active_pokemon = my_state["active"][0]
            active_id = _get_id(active_pokemon)
            if active_id is not None:
                try:
                    from agents.card_registry import CardRegistry
                    card_entry = CardRegistry().get_full_skill(active_id)
                    if card_entry: my_active_damage = card_entry.damage_output
                except Exception as ex:
                    logger.error(f"Error checking active damage: {ex}")

        game_state = {
            "my_hand": [i for i in (_get_id(c) for c in my_state.get("hand", [])) if i is not None] if my_state.get("hand") else [],
            "my_deck_count": my_state.get("deckCount", 60),
            "my_prizes": len(my_state.get("prize", [])) if isinstance(my_state.get("prize"), list) else 6,
            "my_active_pokemon": my_state.get("active", [None])[0] if my_state.get("active") else None,
            "my_bench": my_state.get("bench", []),
            "my_discard": [i for i in (_get_id(c) for c in my_state.get("discard", [])) if i is not None] if my_state.get("discard") else [],
            "my_board": my_board_ids,
            "my_active_damage": my_active_damage,
            "opponent_active": opp_state.get("active", [None])[0] if opp_state.get("active") else None,
            "opponent_bench_count": len(opp_state.get("bench", [])) if opp_state.get("bench") else 0,
            "opponent_prizes": len(opp_state.get("prize", [])) if isinstance(opp_state.get("prize"), list) else 6,
            "opponent_discard": [i for i in (_get_id(c) for c in opp_state.get("discard", [])) if i is not None] if opp_state.get("discard") else [],
            "opponent_revealed": [],
            "opponent_last_play": None,
            "turn_number": current.get("turn", 1),
            "my_active_hp": (my_state.get("active")[0].get("hp", 100) if my_state.get("active") and len(my_state.get("active")) > 0 and my_state.get("active")[0] is not None else 100),
            "opponent_active_hp": (opp_state.get("active")[0].get("hp", 100) if opp_state.get("active") and len(opp_state.get("active")) > 0 and opp_state.get("active")[0] is not None else 100),
            "bench_has_attacker": False,
            "has_searched_deck": getattr(my_state, "has_searched_deck", False),
        }

        # Parse legal candidates from options
        game_state["legal_attacks"] = [opt.get("name", "") for opt in options if opt.get("type") == 13]
        game_state["legal_attachments"] = [opt.get("name", "") for opt in options if opt.get("type") == 9]
        game_state["legal_bench"] = [opt.get("name", "") for opt in options if opt.get("type") == 8]
        game_state["legal_evolutions"] = [opt.get("name", "") for opt in options if opt.get("type") == 10]
        game_state["legal_trainers"] = [opt.get("name", "") for opt in options if opt.get("type") == 7]
        game_state["legal_retreats"] = [opt.get("name", "") for opt in options if opt.get("type") == 12]
        
        sel_type = select.get("type")
        sel_ctx = select.get("context")
        
        game_state["select_prize"] = True if sel_ctx in ("prize", "select_prize") or sel_type == 2 else False

        if (sel_type == 0 and sel_ctx == 0) or game_state["select_prize"]:
            action_label = orchestrator.run_turn(game_state)
            if hasattr(action_label, 'primary_action'):
                action_label = action_label.primary_action
            mapped_indices = get_mapped_indices(action_label, options)
            if not mapped_indices: mapped_indices = [0]

            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count: break
            return selected
        else:
            return fallback_action
    except Exception as e:
        logger.error(f"Error resolving agent choice: {e}")
        return fallback_action
