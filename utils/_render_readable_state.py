import json

def _render_readable_state(pyspiel_state: pyspiel.State) -> str:
    """Build the multi-hand session view that goes into ``{readable_state_str}``.

    Replicates ``RepeatedPokerRethinkAgent._get_prompt_substitutions``.
    """
    state_dict = json.loads(str(pyspiel_state))
    cfg = _config_for_state(pyspiel_state)

    past_hhs: list[str] = []
    for i, acpc_hh in enumerate(pyspiel_state.acpc_hand_histories()):
        past_hhs.append(_render_past_hand(acpc_hh, (i % 2) + 1, cfg))
    if len(past_hhs) != state_dict["hand_number"]:
        raise ValueError(
            f"Number of past hands {len(past_hhs)} does not match number of"
            f" hands in state (current hand={state_dict['hand_number']})."
        )
    past_hhs_str = "\n\n".join(past_hhs)

    players = [f"Player{i}" for i in range(pyspiel_state.num_players())]
    up_state_dict = json.loads(state_dict["current_universal_poker_json"])
    acpc_state_str = up_state_dict["acpc_state"].split("\n")[0]
    if not acpc_state_str.startswith("STATE:"):
        raise ValueError(f"Expected ACPC state to start with STATE:, got {acpc_state_str}")
    # Pluribus-style player suffix.
    acpc_state_str = acpc_state_str + "::" + "|".join(players)

    hh, _ = hh_utils.parse_acpc_line(
        acpc_state_str,
        cfg=cfg,
        policy=hh_utils.ButtonPolicy(),
        button_index=(state_dict["hand_number"] % 2) + 1,
        hand_id_override=str(state_dict["hand_number"]),
    )
    observer_id = f"Player{pyspiel_state.current_player()}"
    current_hand_str = hh_utils.render_pokersite(hand=hh, observer_id=observer_id, sitename="")
    current_hand_str = f"You are Player{pyspiel_state.current_player()}.\n\n{current_hand_str}"
    return (
        f"You are Player{pyspiel_state.current_player()}.\n\n"
        + "Previously played hands this session:\n\n"
        + past_hhs_str
        + "\n\n"
        + "Current hand:\n\n"
        + current_hand_str
    )

