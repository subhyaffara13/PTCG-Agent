
def parse_scan(response, **options):
    cursor, r = response
    return int(cursor), r

