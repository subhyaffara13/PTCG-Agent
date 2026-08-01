
def parse_response_with_state(
    response: str,
    legal_action_strings: Sequence[str],
    state: pyspiel.State,
) -> ParseResult:
    """Parse with a pre-deserialized state. Same as ``parse_response`` but
    skips deserialization -- exposed for the verify script."""
    raw = _extract_move_from_response(response)
    if raw is None:
        return ParseResult(legal_action=None, raw_action=None)
    player_number = state.current_player()
    matched = _soft_parse_poker_action(raw, legal_action_strings, state, player_number)
    if matched is not None and matched in legal_action_strings:
        return ParseResult(legal_action=matched, raw_action=raw)
    return ParseResult(legal_action=None, raw_action=raw)

