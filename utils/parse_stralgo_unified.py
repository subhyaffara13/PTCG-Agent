
def parse_stralgo_unified(response, **options):
    """
    Parse STRALGO into the approved unified shape.

    The legacy parser returns tuple ranges for IDX responses. Unified
    responses use list ranges so RESP2 and RESP3 produce the same value.
    """
    if options.get("len", False):
        return int(response)
    if options.get("idx", False):
        if options.get("withmatchlen", False):
            matches = [
                [int(match[-1])] + [list(m) for m in match[:-1]]
                for match in response[1]
            ]
        else:
            matches = [[list(m) for m in match] for match in response[1]]
        return {
            str_if_bytes(response[0]): matches,
            str_if_bytes(response[2]): int(response[3]),
        }
    return str_if_bytes(response)

