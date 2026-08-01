
def _tcp_rendezvous_handler(
    url: str, timeout: timedelta = default_pg_timeout, **kwargs
):
    def _error(msg):
        return _rendezvous_error("tcp:// rendezvous: " + msg)

    result = urlparse(url)
    if result.port is None:
        raise _error("port number missing")
    query_dict = _query_to_dict(result.query)
    if "rank" not in query_dict:
        raise _error("rank parameter missing")
    if "world_size" not in query_dict:
        raise _error("world size parameter missing")

    rank = int(query_dict["rank"])
    world_size = int(query_dict["world_size"])
    use_libuv = _get_use_libuv_from_query_dict(query_dict)

    if result.hostname is None:
        raise AssertionError("hostname cannot be None")

    store = _create_c10d_store(
        result.hostname, result.port, rank, world_size, timeout, use_libuv
    )

    yield (store, rank, world_size)

    # If this configuration is invalidated, there is nothing we can do about it
    raise RuntimeError("Unable to perform re-rendezvous using tcp:// method")

