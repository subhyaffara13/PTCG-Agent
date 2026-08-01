
def parse_sentinel_master_unified(response, **options):
    state = parse_sentinel_state(map(str_if_bytes, response))
    state["flags"] = set(state["flags"].split(","))
    return state

