
def create_backend(params: RendezvousParameters) -> tuple[C10dRendezvousBackend, Store]:
    """Create a new :py:class:`C10dRendezvousBackend` from the specified parameters.

    +--------------+-----------------------------------------------------------+
    | Parameter    | Description                                               |
    +==============+===========================================================+
    | store_type   | The type of the C10d store. The currently supported types |
    |              | are "tcp" and "file" which correspond to                  |
    |              | :py:class:`torch.distributed.TCPStore` and                |
    |              | :py:class:`torch.distributed.FileStore`, respectively.    |
    |              | Defaults to "tcp".                                        |
    +--------------+-----------------------------------------------------------+
    | read_timeout | The read timeout, in seconds, for store operations.       |
    |              | Defaults to 60 seconds.                                   |
    |              |                                                           |
    |              | Note this only applies to                                 |
    |              | :py:class:`torch.distributed.TCPStore`. It is not relevant|
    |              | to :py:class:`torch.distributed.FileStore` which does not |
    |              | take in timeout as a parameter.                           |
    +--------------+-----------------------------------------------------------+
    | is_host      | A boolean value indicating whether this backend instance  |
    |              | will host the C10d store. If not specified it will be     |
    |              | inferred heuristically by matching the hostname or the IP |
    |              | address of this machine against the specified rendezvous  |
    |              | endpoint. Defaults to ``None``.                           |
    |              |                                                           |
    |              | Note that this configuration option only applies to       |
    |              | :py:class:`torch.distributed.TCPStore`. In normal         |
    |              | circumstances you can safely skip it; the only time when  |
    |              | it is needed is if its value cannot be correctly          |
    |              | determined (e.g. the rendezvous endpoint has a CNAME as   |
    |              | the hostname or does not match the FQDN of the machine).  |
    +--------------+-----------------------------------------------------------+
    """
    # As of today we only support TCPStore and FileStore. Other store types do
    # not have the required functionality (e.g. compare_set) yet.
    store_type = params.get("store_type", "tcp").strip().lower()
    store: Store

    try:
        if store_type == "file":
            store = _create_file_store(params)
        elif store_type == "tcp":
            store = _create_tcp_store(params)
        else:
            raise ValueError(
                "Invalid store type given. Currently only supports file and tcp."
            )

        backend = C10dRendezvousBackend(store, params.run_id)

    except Exception as e:
        construct_and_record_rdzv_event(
            message=f"{type(e).__name__}: {str(e)}",
            run_id=params.run_id,
            node_state=NodeState.FAILED,
        )
        raise

    return backend, store


def create_backend(params: RendezvousParameters) -> tuple[EtcdRendezvousBackend, Store]:
    """Create a new :py:class:`EtcdRendezvousBackend` from the specified parameters.

    +--------------+-----------------------------------------------------------+
    | Parameter    | Description                                               |
    +==============+===========================================================+
    | read_timeout | The read timeout, in seconds, for etcd operations.        |
    |              | Defaults to 60 seconds.                                   |
    +--------------+-----------------------------------------------------------+
    | protocol     | The protocol to use to communicate with etcd. Valid       |
    |              | values are "http" and "https". Defaults to "http".        |
    +--------------+-----------------------------------------------------------+
    | ssl_cert     | The path to the SSL client certificate to use along with  |
    |              | HTTPS. Defaults to ``None``.                              |
    +--------------+-----------------------------------------------------------+
    | ssl_cert_key | The path to the private key of the SSL client certificate |
    |              | to use along with HTTPS. Defaults to ``None``.            |
    +--------------+-----------------------------------------------------------+
    | ca_cert      | The path to the rool SSL authority certificate. Defaults  |
    |              | to ``None``.                                              |
    +--------------+-----------------------------------------------------------+
    """
    client = _create_etcd_client(params)

    backend = EtcdRendezvousBackend(
        client, params.run_id, key_prefix="/torch/elastic/rendezvous"
    )

    store = EtcdStore(client, "/torch/elastic/store")

    return backend, store

