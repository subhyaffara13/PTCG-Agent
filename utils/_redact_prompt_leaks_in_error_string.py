
def _redact_prompt_leaks_in_error_string(text: str) -> str:
    """
    Strip echoed request input from provider error strings.

    Provider validation errors (e.g. OpenAI ``RateLimitError`` carrying 178
    pydantic validation errors, each with its own ``'input': [...]`` field)
    embed the full request body in their message. When prompts must not be
    stored in spend logs, that echo is a back-door leak.

    Two leak shapes are handled:

    - Quoted-key form — ``"<key>": <value>`` where ``key`` is ``input``,
      ``messages`` or ``prompt`` (covers JSON bodies, Python dict-reprs,
      and ``/v1/completions`` payloads).
    - Assignment form — ``input_value=<value>`` from Pydantic v2 validation
      errors, which render the offending value as a Python repr inside
      ``[type=..., input_value=..., input_type=...]``.

    The value scan understands nested ``[]`` / ``{}`` and quoted strings,
    so multi-modal payloads (``'messages': [{'content': [{...}]}]``) and
    user text containing brackets (``"secret[123"``) are handled correctly.
    """
    if not text:
        return text
    redaction = f'"{REDACTED_BY_LITELM_STRING}"'
    out: List[str] = []
    n = len(text)
    pos = 0
    while pos < n:
        m = _SENSITIVE_KEY_START_PATTERN.search(text, pos)
        if not m:
            out.append(text[pos:])
            break
        out.append(text[pos : m.end()])
        v_start = m.end()
        if v_start >= n:
            break
        first = text[v_start]
        if first in ("[", "{", "'", '"'):
            v_end = _scan_balanced_value_end(text, v_start)
            if v_end == -1:
                # Unterminated value — redact through the rest of the string
                # so a malformed leak can't slip past.
                out.append(redaction)
                pos = n
                break
            out.append(redaction)
            pos = v_end
        else:
            # Unquoted scalar (number, null, bare identifier) — not a leak
            # carrier, leave intact and resume after the key match.
            pos = v_start
    return "".join(out)

