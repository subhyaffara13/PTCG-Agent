
def extract_last_json_object(
    response: str,
    *,
    required_keys: Sequence[str] | None = None,
) -> dict[str, Any] | None:
    """Find the LAST parseable JSON object in an LLM response.

    Models routinely write a preliminary answer, reconsider, and write a
    final answer in a later block. Returning the *last* parseable object
    follows the model's last stated intent. Searching the first match
    instead (the common bug this helper exists to prevent) silently picks
    the rejected answer.

    Two strategies are tried in priority order; the FIRST strategy that
    yields any parseable dict wins, and the LAST candidate from that
    strategy is returned:

    1. ``` ```json ... ``` ``` (and unlabelled ``` ``` ``` ```) fenced blocks.
    2. Balanced top-level ``{...}`` substrings, parsed with
       ``json.JSONDecoder.raw_decode`` so nested objects work correctly.

    Args:
        response: The full LLM response text.
        required_keys: If given, candidates lacking every one of these keys
            at the top level are skipped. Lets callers ignore JSON-shaped
            content in the model's reasoning that isn't an action object.

    Returns:
        The matching dict, or ``None`` if no candidate parses.
    """

    def _passes_filter(d: dict[str, Any]) -> bool:
        if required_keys is None:
            return True
        return any(k in d for k in required_keys)

    fenced: list[dict[str, Any]] = []
    for match in _JSON_FENCE_RE.finditer(response):
        try:
            obj = json.loads(match.group(1), strict=False)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and _passes_filter(obj):
            fenced.append(obj)
    if fenced:
        return fenced[-1]

    bare: list[dict[str, Any]] = []
    i = 0
    while True:
        i = response.find("{", i)
        if i < 0:
            break
        try:
            obj, end = _JSON_DECODER.raw_decode(response, i)
        except json.JSONDecodeError:
            i += 1
            continue
        if isinstance(obj, dict) and _passes_filter(obj):
            bare.append(obj)
        i = end
    if bare:
        return bare[-1]

    return None

