
def _get_best_family(address, port):
    """Automatically select address family depending on address"""
    # HTTPServer defaults to AF_INET, which will not start properly if
    # binding an ipv6 address is requested.
    # This function is based on what upstream python did for http.server
    # in https://github.com/python/cpython/pull/11767
    infos = socket.getaddrinfo(address, port, type=socket.SOCK_STREAM, flags=socket.AI_PASSIVE)
    family, _, _, _, sockaddr = next(iter(infos))
    return family, sockaddr[0]

