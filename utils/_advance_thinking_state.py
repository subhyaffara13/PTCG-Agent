
def _advance_thinking_state(streamer, token_id: int) -> bool:
    """Mutate ``streamer``'s thinking state; return ``True`` if ``token_id`` is a start or end token.

    Shared between :class:`DirectStreamer` and :class:`CBStreamer` — both track the
    same four attributes (``_thinking_start_ids``, ``_thinking_end_id``,
    ``_inside_thinking``, ``_thinking_prefix``) and need identical edge handling.
    """
    if streamer._thinking_start_ids is None:
        return False
    if streamer._inside_thinking:
        if token_id == streamer._thinking_end_id:
            streamer._inside_thinking = False
            return True
        return False
    expected = streamer._thinking_start_ids[len(streamer._thinking_prefix)]
    if token_id != expected:
        streamer._thinking_prefix = []
        return False
    streamer._thinking_prefix.append(token_id)
    if len(streamer._thinking_prefix) == len(streamer._thinking_start_ids):
        streamer._inside_thinking = True
        streamer._thinking_prefix = []
    return True

