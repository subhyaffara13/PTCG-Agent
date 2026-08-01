
def parse_sentinel_slaves_and_sentinels(response, **options):
    return [parse_sentinel_state(map(str_if_bytes, item)) for item in response]

