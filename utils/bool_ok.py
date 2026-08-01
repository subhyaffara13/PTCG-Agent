
def bool_ok(response, **options):
    return str_if_bytes(response) == "OK"

