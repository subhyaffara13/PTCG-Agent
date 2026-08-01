
def _build_game_state_from_observation(my_state, opp_state, current, select):
    from factory.game_adapter_state import build_game_state
    game_state = build_game_state(my_state, opp_state, current)
    options = select.get("options") or select.get("option") or []
    game_state["legal_attacks"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (12, 13)]
    game_state["legal_attachments"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (8, 9)]
    sel_type = select.get("type"); sel_ctx = select.get("context")
    game_state["select_prize"] = bool(sel_ctx in ("prize", "select_prize") or sel_type == 2)
    game_state["select_type"] = sel_type; game_state["select_context"] = sel_ctx
    return game_state

