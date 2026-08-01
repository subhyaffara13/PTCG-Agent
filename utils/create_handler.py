
def create_handler(
    store: Store, backend: RendezvousBackend, params: RendezvousParameters
) -> DynamicRendezvousHandler:
    """Create a new :py:class:`DynamicRendezvousHandler` from the specified parameters.

    Args:
        store:
            The C10d store to return as part of the rendezvous.
        backend:
            The backend to use to hold the rendezvous state.

    +-------------------+------------------------------------------------------+
    | Parameter         | Description                                          |
    +===================+======================================================+
    | join_timeout      | The total time, in seconds, within which the         |
    |                   | rendezvous is expected to complete. Defaults to 600  |
    |                   | seconds.                                             |
    +-------------------+------------------------------------------------------+
    | last_call_timeout | An additional wait amount, in seconds, before        |
    |                   | completing the rendezvous once the minimum number of |
    |                   | nodes has been reached. Defaults to 30 seconds.      |
    +-------------------+------------------------------------------------------+
    | close_timeout     | The time, in seconds, within which the rendezvous is |
    |                   | expected to close after a call to                    |
    |                   | :py:meth:`RendezvousHandler.set_closed` or           |
    |                   | :py:meth:`RendezvousHandler.shutdown`. Defaults to   |
    |                   | 30 seconds.                                          |
    +-------------------+------------------------------------------------------+
    | heartbeat         | The time, in seconds, within which a keep-alive      |
    |                   | heartbeat is expected to complete                    |
    +-------------------+------------------------------------------------------+
    """
    try:
        timeout = RendezvousTimeout(
            _get_timeout(params, "join"),
            _get_timeout(params, "last_call"),
            _get_timeout(params, "close"),
            _get_timeout(params, "heartbeat"),
        )
        keep_alive_interval = params.get_as_int("keep_alive_interval", 5)
        if keep_alive_interval is None:
            raise TypeError(
                "You passed 'keep_alive_interval=None' as a rendezvous configuration option"
            )
        keep_alive_max_attempt = params.get_as_int("keep_alive_max_attempt", 3)
        if keep_alive_max_attempt is None:
            raise TypeError(
                "You passed 'keep_alive_max_attempt=None' as a rendezvous configuration option"
            )

        return DynamicRendezvousHandler.from_backend(
            params.run_id,
            store,
            backend,
            params.min_nodes,
            params.max_nodes,
            params.local_addr,
            timeout,
            keep_alive_interval=keep_alive_interval,
            keep_alive_max_attempt=keep_alive_max_attempt,
        )
    except Exception as e:
        construct_and_record_rdzv_event(
            message=f"{type(e).__name__}: {str(e)}",
            run_id=params.run_id,
            node_state=NodeState.FAILED,
        )
        raise

