
def build_context(observation: Mapping[str, Any]) -> PromptContext:
    """Parse the observation into a :class:`PromptContext`.

    Lives here (not in harness_experiment.py) so variant build functions
    can also be exercised directly from tests or a sweep runner.
    """
    state = parse_observation_payload(observation)
    player_id = int(observation.get("playerId", 0))

    pool = state.get("pool") or {k: 0 for k in _ITEM_KEYS}
    my_values = state.get("my_values") or {k: 0 for k in _ITEM_KEYS}
    params = state.get("params") or {}
    max_turns = int(params.get("max_turns", state.get("max_turns", 10)))
    discount = float(params.get("discount", 1.0))
    num_offers = int(state.get("num_offers", 0))
    turns_left = max(0, max_turns - num_offers)
    offer_history = state.get("offer_history") or []

    last_offer_event = offer_history[-1] if offer_history else None
    can_accept = bool(
        last_offer_event
        and last_offer_event.get("type") == "offer"
        and int(last_offer_event.get("player", -1)) != player_id
    )

    return PromptContext(
        state=state,
        player_id=player_id,
        pool=pool,
        my_values=my_values,
        max_turns=max_turns,
        discount=discount,
        num_offers=num_offers,
        turns_left=turns_left,
        offer_history=offer_history,
        can_accept=can_accept,
        last_offer_event=last_offer_event,
    )

