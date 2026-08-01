
def _extract_json(response: str) -> dict[str, Any] | None:
    """Pull the LAST action object from the LLM response.

    Cluemaster turns emit a ``{"clue": ..., "number": ...}`` object; guesser
    turns emit a ``{"guess": ...}`` object. We filter by those keys so that
    JSON-shaped content elsewhere in the model's reasoning is ignored.
    """
    return extract_last_json_object(response, required_keys=("clue", "guess"))

