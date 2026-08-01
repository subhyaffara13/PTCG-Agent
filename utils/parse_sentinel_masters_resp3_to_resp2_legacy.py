
def parse_sentinel_masters_resp3_to_resp2_legacy(response, **options):
    result = {}
    for master in response:
        state = parse_sentinel_state(
            map(str_if_bytes, _flatten_resp3_state_pairs(master))
        )
        result[state["name"]] = state
    return result

