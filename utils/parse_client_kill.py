
def parse_client_kill(response, **options):
    if isinstance(response, int):
        return response
    return str_if_bytes(response) == "OK"

