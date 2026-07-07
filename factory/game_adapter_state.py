import logging
from factory.game_adapter_helpers import get_card_id

logger = logging.getLogger(__name__)

def build_game_state(my_state, opp_state, current):
    my_board_ids = []
    for zone in ["active", "bench"]:
        if my_state.get(zone):
            for c in my_state[zone]:
                _id = get_card_id(c)
                if _id is not None: my_board_ids.append(_id)

    my_active_damage = 0
    if my_state.get("active") and len(my_state["active"]) > 0:
        active_pokemon = my_state["active"][0]
        active_id = get_card_id(active_pokemon)
        if active_id is not None:
            try:
                from cb_agents.card_registry import CardRegistry
                card_entry = CardRegistry().get_full_skill(active_id)
                if card_entry: my_active_damage = card_entry.damage_output
            except Exception as ex:
                logger.error(f"Error checking active damage: {ex}")

    game_state = {
        "my_hand": [i for i in (get_card_id(c) for c in my_state.get("hand", [])) if i is not None] if my_state.get("hand") else [],
        "my_deck_count": my_state.get("deckCount", 60),
        "my_prizes": len(my_state.get("prize", [])) if isinstance(my_state.get("prize"), list) else 6,
        "my_active_pokemon": my_state.get("active", [None])[0] if my_state.get("active") else None,
        "my_bench": my_state.get("bench", []),
        "my_discard": [i for i in (get_card_id(c) for c in my_state.get("discard", [])) if i is not None] if my_state.get("discard") else [],
        "my_board": my_board_ids,
        "my_active_damage": my_active_damage,
        "opponent_active": opp_state.get("active", [None])[0] if opp_state.get("active") else None,
        "opponent_bench_count": len(opp_state.get("bench", [])) if opp_state.get("bench") else 0,
        "opponent_prizes": len(opp_state.get("prize", [])) if isinstance(opp_state.get("prize"), list) else 6,
        "opponent_discard": [i for i in (get_card_id(c) for c in opp_state.get("discard", [])) if i is not None] if opp_state.get("discard") else [],
        "opponent_revealed": [],
        "opponent_last_play": None,
        "turn_number": current.get("turn", 1),
        "my_active_hp": (my_state.get("active")[0].get("hp", 100) if my_state.get("active") and len(my_state.get("active")) > 0 and my_state.get("active")[0] is not None else 100),
        "opponent_active_hp": (opp_state.get("active")[0].get("hp", 100) if opp_state.get("active") and len(opp_state.get("active")) > 0 and opp_state.get("active")[0] is not None else 100),
        "bench_has_attacker": False,
        "has_searched_deck": getattr(my_state, "has_searched_deck", False),
    }
    return game_state
