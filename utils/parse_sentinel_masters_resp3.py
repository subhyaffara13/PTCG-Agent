
def parse_sentinel_masters_resp3(response, **options):
    result = {}
    for master in response:
        state = parse_sentinel_state_resp3(master)
        result[state["name"]] = state
    return result

