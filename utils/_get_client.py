
def _get_client(client):
    if client is None:
        return _get_global_client()
    elif isinstance(client, Client):
        return client
    else:
        # e.g., connection string
        return Client(client)

