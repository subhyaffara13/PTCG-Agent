
def _create_c10d_store(
    hostname, port, rank, world_size, timeout, use_libuv=True
) -> Store:
    """
    Smartly creates a c10d Store object on ``rank`` based on whether we need to reuse agent store.

    The TCPStore server is assumed to be hosted
    on ``hostname:port``.

    By default, the TCPStore server uses the asynchronous implementation
    ``LibUVStoreDaemon`` which utilizes libuv.

    If ``torchelastic_use_agent_store()`` is ``True``, then it is assumed that
    the agent leader (node rank 0) hosts the TCPStore server (for which the
    endpoint is specified by the given ``hostname:port``). Hence
    ALL ranks will create and return a TCPStore client (e.g. ``start_daemon=False``).

    If ``torchelastic_use_agent_store()`` is ``False``, then rank 0 will host
    the TCPStore (with multi-tenancy) and it is assumed that rank 0's hostname
    and port are correctly passed via ``hostname`` and ``port``. All
    non-zero ranks will create and return a TCPStore client.
    """
    # check if port is uint16_t
    if not 0 <= port < 2**16:
        raise ValueError(f"port must have value from 0 to 65535 but was {port}.")

    if _torchelastic_use_agent_store():
        # We create a new TCPStore for every retry so no need to add prefix for each attempt.
        return TCPStore(
            host_name=hostname,
            port=port,
            world_size=world_size,
            is_master=False,
            timeout=timeout,
        )
    else:
        start_daemon = rank == 0
        return TCPStore(
            host_name=hostname,
            port=port,
            world_size=world_size,
            is_master=start_daemon,
            timeout=timeout,
            multi_tenant=True,
            use_libuv=use_libuv,
        )

