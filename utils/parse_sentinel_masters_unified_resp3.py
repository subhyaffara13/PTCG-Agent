
def parse_sentinel_masters_unified_resp3(response, **options):
    result = {}
    for master in response:
        state = parse_sentinel_state_resp3(master)
        _add_derived_sentinel_booleans(state, state["flags"])
        result[state["name"]] = state
    return result

