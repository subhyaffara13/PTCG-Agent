
def parse_sentinel_slaves_and_sentinels_resp3_to_resp2_legacy(response, **options):
    return [
        parse_sentinel_state(map(str_if_bytes, _flatten_resp3_state_pairs(item)))
        for item in response
    ]

