
def _get_addr_and_port(
    rdzv_parameters: RendezvousParameters,
) -> tuple[str | None, int | None]:
    if rdzv_parameters.backend != "static":
        return (None, None)
    endpoint = rdzv_parameters.endpoint
    endpoint = endpoint.strip()
    if not endpoint:
        raise ValueError(
            "Endpoint is missing in endpoint. Try to add --master-addr and --master-port"
        )
    master_addr, master_port = parse_rendezvous_endpoint(endpoint, default_port=-1)
    if master_port == -1:
        raise ValueError(
            f"port is missing in endpoint: {endpoint}. Try to specify --master-port"
        )
    return (master_addr, master_port)

