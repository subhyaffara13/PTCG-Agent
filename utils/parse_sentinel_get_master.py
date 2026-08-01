
def parse_sentinel_get_master(response, **options):
    return response and (response[0], int(response[1])) or None

