
def parse_sentinel_master(response, **options):
    return parse_sentinel_state(map(str_if_bytes, response))

