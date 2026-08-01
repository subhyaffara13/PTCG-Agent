
def _get_direct_client_ip(request: Request) -> Optional[str]:
    client = getattr(request, "client", None)
    client_host = getattr(client, "host", None)
    if isinstance(client_host, str):
        return client_host
    return None

