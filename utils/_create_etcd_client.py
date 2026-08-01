
def _create_etcd_client(params: RendezvousParameters) -> etcd.Client:
    """Create a new ``etcd.Client`` from the specified ``RendezvousParameters``."""
    hostname, port = parse_rendezvous_endpoint(params.endpoint, 2379)

    # The communication protocol
    protocol = params.config.get("protocol")
    if protocol is None:
        protocol = "http"
    else:
        if protocol != "http" and protocol != "https":
            raise ValueError("The etcd protocol must be HTTP or HTTPS.")

    # The SSL client certificate
    ssl_cert = params.config.get("cert")
    if ssl_cert is not None:
        cert_key = params.config.get("key")
        if cert_key is not None:
            # The etcd client expects the certificate key as the second element
            # of the `cert` tuple.
            ssl_cert = (ssl_cert, cert_key)

    # The root certificate
    ca_cert = params.config.get("cacert")

    return etcd.Client(
        hostname,
        port,
        protocol=protocol,
        cert=ssl_cert,
        ca_cert=ca_cert,
        allow_reconnect=True,
    )


def _create_etcd_client(params: RendezvousParameters) -> etcd.Client:
    host, port = parse_rendezvous_endpoint(params.endpoint, default_port=2379)

    # The timeout
    read_timeout = cast(int, params.get_as_int("read_timeout", 60))
    if read_timeout <= 0:
        raise ValueError("The read timeout must be a positive integer.")

    # The communication protocol
    protocol = params.get("protocol", "http").strip().lower()
    if protocol != "http" and protocol != "https":
        raise ValueError("The protocol must be HTTP or HTTPS.")

    # The SSL client certificate
    ssl_cert = params.get("ssl_cert")
    if ssl_cert:
        ssl_cert_key = params.get("ssl_cert_key")
        if ssl_cert_key:
            # The etcd client expects the certificate key as the second element
            # of the `cert` tuple.
            ssl_cert = (ssl_cert, ssl_cert_key)

    # The root certificate
    ca_cert = params.get("ca_cert")

    try:
        return etcd.Client(
            host,
            port,
            read_timeout=read_timeout,
            protocol=protocol,
            cert=ssl_cert,
            ca_cert=ca_cert,
            allow_reconnect=True,
        )
    except (etcd.EtcdException, urllib3.exceptions.TimeoutError) as exc:
        raise RendezvousConnectionError(
            "The connection to etcd has failed. See inner exception for details."
        ) from exc

