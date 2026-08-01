
def parse_sentinel_slaves_and_sentinels_resp3(response, **options):
    return [parse_sentinel_state_resp3(item, **options) for item in response]

