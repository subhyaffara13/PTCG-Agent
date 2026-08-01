
def _cookie_unslash_replace(m: t.Match[bytes]) -> bytes:
    v = m.group(1)

    if len(v) == 1:
        return v

    return int(v, 8).to_bytes(1, "big")

