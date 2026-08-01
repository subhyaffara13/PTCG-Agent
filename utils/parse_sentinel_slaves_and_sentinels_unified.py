
def parse_sentinel_slaves_and_sentinels_unified(response, **options):
    out = []
    for item in response:
        state = parse_sentinel_state(map(str_if_bytes, item))
        state["flags"] = set(state["flags"].split(","))
        out.append(state)
    return out

