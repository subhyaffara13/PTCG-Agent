
def parse_sentinel_masters_unified(response, **options):
    result = {}
    for item in response:
        state = parse_sentinel_state(map(str_if_bytes, item))
        state["flags"] = set(state["flags"].split(","))
        result[state["name"]] = state
    return result

