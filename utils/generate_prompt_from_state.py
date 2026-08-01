
def generate_prompt_from_state(
    state: pyspiel.State,
    previous_response: str | None = None,
) -> str:
    """Build the LLM prompt from a pre-deserialized pyspiel state.

    Exposed so the verify script can replay the game forward, deserializing
    once instead of per-prompt.
    """
    readable_state_str = _render_readable_state(state)

    if previous_response is None:
        rethink_prompt = ""
    else:
        # Upstream POKER_RETHINK uses the last 5 lines of the prior generation,
        # or "NO RESPONSE RECEIVED" if empty.
        if not previous_response:
            generation = "NO RESPONSE RECEIVED"
        else:
            generation = "\n".join(previous_response.split("\n")[-5:])
        rethink_prompt = POKER_RETHINK.format(generation=generation)

    return REPEATED_POKER.format(
        readable_state_str=readable_state_str,
        rethink_prompt=rethink_prompt,
    )

