
def parse_acl_log_resp3_unified(response, **options):
    """Parse RESP3 ACL LOG into the approved unified shape."""
    if response is None:
        return None
    if not isinstance(response, list):
        return bool_ok(response)
    data = []
    for entry in response:
        if isinstance(entry, dict):
            log_data = {str_if_bytes(k): v for k, v in entry.items()}
        else:
            log_data = pairs_to_dict(entry, True, True)
        if "age-seconds" in log_data:
            log_data["age-seconds"] = float(log_data["age-seconds"])
        if "client-info" in log_data:
            log_data["client-info"] = parse_client_info(log_data["client-info"])
        for key, value in list(log_data.items()):
            if key not in ("age-seconds", "client-info"):
                log_data[key] = str_if_bytes(value)
        data.append(log_data)
    return data

