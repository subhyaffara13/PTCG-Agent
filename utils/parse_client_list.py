
def parse_client_list(response, **options):
    clients = []
    for c in str_if_bytes(response).splitlines():
        client_dict = {}
        tokens = c.split(" ")
        last_key = None
        for token in tokens:
            if "=" in token:
                # Values might contain '='
                key, value = token.split("=", 1)
                client_dict[key] = value
                last_key = key
            else:
                # Values may include spaces. For instance, when running Redis via a Unix socket — such as
                # "/tmp/redis sock/redis.sock" — the addr or laddr field will include a space.
                client_dict[last_key] += " " + token

        if client_dict:
            clients.append(client_dict)
    return clients

