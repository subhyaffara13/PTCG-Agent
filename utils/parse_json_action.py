
def parse_json_action(
    response: str,
    legal_action_strings: Sequence[str],
    *,
    json_key: str = "move",
    matcher: Callable[[str, Sequence[str]], str | None] | None = None,
) -> ParseResult:
    """Default ``parse_response`` body for enumerable harnesses.

    The model's stated intent is the value of ``json_key`` in the LAST
    parseable JSON object in the response. This helper:

    1. Extracts that value via ``extract_last_json_object``. If no JSON
       answer is present, returns ``ParseResult(legal_action=None,
       raw_action=None)`` so the rethink loop asks the model for one.
    2. Matches the value against ``legal_action_strings`` (case-insensitive
       and whitespace-stripped by default; pass ``matcher`` for game-
       specific normalization, e.g. notation tolerance or alias handling).
    3. Always returns the raw extracted value as ``raw_action`` -- when the
       JSON is illegal, ``legal_action`` is ``None`` and the rethink prompt
       can show the model what it tried so it can correct itself.

    The helper deliberately has NO prose-scan fallback. Any "guess at
    intent from a coord/keyword/legal-string mentioned in the prose" path
    is the ghost-fallback antipattern: it silently submits moves the model
    never explicitly chose (usually rejected options it discussed in its
    reasoning). The rethink loop is the right way to handle illegal or
    missing structured answers.

    Args:
        response: The full LLM response text.
        legal_action_strings: The legal moves to match against.
        json_key: Top-level JSON field carrying the move (default ``"move"``).
        matcher: Optional ``(raw, legals) -> matched | None`` for game-
            specific normalization. If omitted, exact case-insensitive
            whitespace-stripped matching is used.

    Returns:
        ``ParseResult(legal_action=matched_or_None, raw_action=raw_or_None)``.
    """
    data = extract_last_json_object(response, required_keys=(json_key,))
    if data is None:
        return ParseResult(legal_action=None, raw_action=None)
    raw_value = data.get(json_key)
    if raw_value is None:
        return ParseResult(legal_action=None, raw_action=None)
    raw = str(raw_value).strip()
    if not raw:
        return ParseResult(legal_action=None, raw_action=None)
    if matcher is None:
        matched = _default_match(raw, legal_action_strings)
    else:
        matched = matcher(raw, legal_action_strings)
    return ParseResult(legal_action=matched, raw_action=raw)

