
def _get_all_pg_configs() -> list[dict[str, Any]]:
    """
    Return the pg configuration of all the process groups.

    """
    config_info: list[dict[str, Any]] = [_get_pg_config(pg) for pg in _world.pg_map]
    return config_info

