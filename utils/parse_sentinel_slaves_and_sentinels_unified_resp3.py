
def parse_sentinel_slaves_and_sentinels_unified_resp3(response, **options):
    out = []
    for item in response:
        state = parse_sentinel_state_resp3(item, **options)
        _add_derived_sentinel_booleans(state, state["flags"])
        out.append(state)
    return out

