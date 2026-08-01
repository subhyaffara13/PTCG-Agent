
def parse_sentinel_master_unified_resp3(response, **options):
    state = parse_sentinel_state_resp3(response, **options)
    _add_derived_sentinel_booleans(state, state["flags"])
    return state

