
def parse_sentinel_state_resp3(response, **options):
    result = {}
    for key in response:
        str_key = str_if_bytes(key)
        try:
            value = SENTINEL_STATE_TYPES[str_key](str_if_bytes(response[key]))
            result[str_key] = value
        except Exception:
            result[str_key] = str_if_bytes(response[key])
    flags = set(result["flags"].split(","))
    result["flags"] = flags
    _add_derived_sentinel_booleans(result, flags)
    return result

