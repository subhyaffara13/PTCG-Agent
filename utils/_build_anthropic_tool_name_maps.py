
def _build_anthropic_tool_name_maps(
    original_names: List[str],
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Build (forward, reverse) tool-name maps for a single request.

    forward[original] = sanitized   -- only present when name was rewritten
    reverse[sanitized] = original   -- inverse of `forward`

    Properties:
    - All sanitized names satisfy ^[a-zA-Z0-9_-]{1,128}$.
    - Sanitized names are unique within the request (no two originals
      collide on the wire).
    - A name that's already valid AND doesn't collide with another tool's
      sanitized form passes through untouched and is absent from the maps.
      That's the key correctness property: response-side translation only
      runs on entries we actually rewrote, so a tool legitimately named
      `foo_bar` is never incorrectly retyped to `foo/bar` just because
      some *other* request had that pair.
    - Order-dependent: when two originals would clash, the *second* one
      seen gets the disambiguating suffix. Callers should preserve the
      caller's tool order (we do).
    """
    forward: Dict[str, str] = {}
    used: set = set()

    # First pass: reserve slots for names that are already valid so they
    # always have priority regardless of input order.
    for original in original_names:
        if not isinstance(original, str) or not original:
            continue
        candidate = _basic_sanitize_anthropic_tool_name(original)
        if candidate == original:
            used.add(candidate)

    # Second pass: sanitize/disambiguate names that need rewriting.
    for original in original_names:
        if not isinstance(original, str) or not original:
            continue
        candidate = _basic_sanitize_anthropic_tool_name(original)
        if candidate == original:
            continue
        # Skip duplicates of the same original name. Without this guard the
        # second pass would assign a fresh suffix and overwrite the forward
        # map entry, causing every reference to map to the suffixed name and
        # leaving the original sanitized slot orphaned in `used` with no
        # reverse mapping.
        if original in forward:
            continue
        # Disambiguate against names already chosen this request.
        unique = candidate
        n = 1
        while unique in used:
            n += 1
            suffix = f"_{n}"
            # Keep within the 128-char cap.
            head = candidate[: _ANTHROPIC_TOOL_NAME_MAX_LEN - len(suffix)]
            unique = f"{head}{suffix}"
        forward[original] = unique
        used.add(unique)
    reverse = {v: k for k, v in forward.items()}
    return forward, reverse

