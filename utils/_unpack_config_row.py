
def _unpack_config_row(cached: Any) -> Optional[_ConfigRow]:
    if cached is None or cached == _CONFIG_CACHE_MISS:
        return None
    if isinstance(cached, dict):
        return _ConfigRow(cached["param_name"], cached["param_value"])
    return None

