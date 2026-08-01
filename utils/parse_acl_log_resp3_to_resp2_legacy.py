
def parse_acl_log_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire ACL LOG → today's RESP2 parsed shape.

    Each log entry arrives as a ``dict`` on RESP3 wire instead of a flat
    list of pairs; convert ``client-info`` from a string blob into the
    parsed ``dict`` and ``age-seconds`` to ``float`` so the Python shape
    matches what :func:`parse_acl_log` produces from RESP2 wire.

    Also used as the unified callback (Set D): the legacy and unified
    shapes coincide for ACL LOG.
    """
    if response is None:
        return None
    if not isinstance(response, list):
        return bool_ok(response)
    data = []
    for log in response:
        if isinstance(log, dict):
            log_data = {str_if_bytes(k): v for k, v in log.items()}
        else:
            log_data = pairs_to_dict(log, True, True)
        client_info = log_data.get("client-info", "")
        log_data["client-info"] = parse_client_info(client_info)
        log_data["age-seconds"] = float(log_data["age-seconds"])
        data.append(log_data)
    return data

