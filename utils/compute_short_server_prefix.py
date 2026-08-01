
def compute_short_server_prefix(server_id: str, attempt: int = 0) -> str:
    """Derive the deterministic three-character prefix for a server.

    Uses SHA-256 of ``f"{server_id}#{attempt}"`` and folds the first eight
    bytes into a fixed-length string whose first character is drawn from
    ``_BASE52_ALPHA_ALPHABET`` (so the prefix never starts with a digit)
    and whose remaining characters are drawn from the full base62
    alphabet.  Pass ``attempt > 0`` to rehash to a different prefix when
    the natural hash collides with a prefix already assigned to another
    server (see ``MCPServerManager._assign_unique_short_prefix``).  An
    empty ``server_id`` raises ``ValueError`` — short prefixes require a
    stable identifier to be deterministic.
    """
    if not server_id:
        raise ValueError("compute_short_server_prefix requires a non-empty server_id")

    seed = server_id if attempt == 0 else f"{server_id}#{attempt}"
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    value = int.from_bytes(digest[:8], "big")

    # Build chars from least-significant to most-significant; we reverse
    # at the end so the first emitted char comes from the high-order
    # bits of the digest (which is the position we constrain to be
    # alphabetic).
    chars = []
    for position in range(SHORT_MCP_TOOL_PREFIX_LENGTH):
        is_first_char = position == SHORT_MCP_TOOL_PREFIX_LENGTH - 1
        alphabet = _BASE52_ALPHA_ALPHABET if is_first_char else _BASE62_ALPHABET
        value, idx = divmod(value, len(alphabet))
        chars.append(alphabet[idx])
    return "".join(reversed(chars))

