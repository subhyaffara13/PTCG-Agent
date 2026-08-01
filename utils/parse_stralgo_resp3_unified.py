
def parse_stralgo_resp3_unified(response, **options):
    """Parse RESP3 STRALGO into the same value as ``parse_stralgo_unified``."""
    if options.get("len", False):
        return int(response)
    if options.get("idx", False):
        if not isinstance(response, dict):
            return str_if_bytes(response)
        raw_matches = response.get("matches", response.get(b"matches", []))
        raw_len = response.get("len", response.get(b"len", 0))
        if options.get("withmatchlen", False):
            matches = [
                [int(match[-1])] + [list(m) for m in match[:-1]]
                for match in raw_matches
            ]
        else:
            matches = [[list(m) for m in match] for match in raw_matches]
        return {"matches": matches, "len": int(raw_len)}
    return str_if_bytes(response)

