
def parse_hscan(response, **options):
    cursor, r = response
    no_values = options.get("no_values", False)
    if no_values:
        payload = r or []
    else:
        payload = r and pairs_to_dict(r) or {}
    return int(cursor), payload

