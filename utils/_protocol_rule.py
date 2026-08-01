
def _protocol_rule(state: StateInline, silent: bool) -> bool:
    if state.linkLevel > 0:
        return False

    pos = state.pos
    remaining = state.src[pos : state.posMax]

    # Must start with ':' and have at least 3 more characters.
    if len(remaining) < 4 or remaining[0] != ":":
        return False

    # Back-scan pending text for a known protocol name.
    m = _PROTO_RE.search(state.pending)
    if m is None:
        return False

    proto = m.group(1)
    bscan_len = len(proto)

    if not _preceding_ok(state, bscan_len):
        return False

    # Combine back-scanned protocol with the remaining text.
    combined = proto + remaining

    if proto in ("mailto", "xmpp"):
        result = match_any_email(combined, bscan_len + 1, proto)
    else:
        result = match_http(combined)

    if result is None:
        return False

    full_url, total_len = result
    label = combined[:total_len]

    if silent:
        return True
    return _create_autolink(state, bscan_len, total_len, full_url, label)

