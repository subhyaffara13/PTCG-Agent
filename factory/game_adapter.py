import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def run_agent_turn(orchestrator, observation: dict, deck: list[int]) -> list[int]:
    """Interactions adapter mapping CABT observations to Orchestrator and actions back to options."""
    select = observation.get("select")
    if select is None:
        return deck

    options = select.get("option", [])
    max_count = select.get("maxCount", 1)
    fallback_action = list(range(min(max_count, len(options))))

    try:
        current = observation.get("current")
        if not current:
            return fallback_action

        my_idx = current.get("yourIndex", 0)
        players = current.get("players", [])
        if len(players) <= my_idx:
            return fallback_action

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}

        def _get_id(c):
            if hasattr(c, "id"): return getattr(c, "id")
            if isinstance(c, dict): return c.get("id")
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
                    if card_entry:
                        my_active_damage = card_entry.damage_output
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
            "bench_has_attacker": False
        }

        # Parse legal candidates from options
        game_state["legal_attacks"] = [opt.get("name", "") for opt in options if opt.get("type") == 13]
        game_state["legal_attachments"] = [opt.get("name", "") for opt in options if opt.get("type") == 9]
        game_state["legal_bench"] = [opt.get("name", "") for opt in options if opt.get("type") == 8]
        game_state["legal_evolutions"] = []
        game_state["legal_trainers"] = [opt.get("name", "") for opt in options if opt.get("type") == 7]

        sel_type = select.get("type")
        sel_ctx = select.get("context")

        if sel_type == 0 and sel_ctx == 0:
            action_label = orchestrator.run_turn(game_state)
            mapped_indices = []
            if action_label.startswith("attack:"):
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 13]
            elif action_label.startswith("attach_energy:"):
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 9]
            elif action_label.startswith("bench:") or action_label.startswith("evolve:"):
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 8]
            elif action_label.startswith("play_trainer:"):
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 7]
            elif action_label.startswith("retreat:"):
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 10]

            if not mapped_indices or action_label == "pass":
                mapped_indices = [i for i, opt in enumerate(options) if opt.get("type") == 14]

            if not mapped_indices:
                mapped_indices = [0]

            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
            return selected
        else:
            return fallback_action
    except Exception as e:
        logger.error(f"Error resolving agent choice: {e}")
        return fallback_action
