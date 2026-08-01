
def _add_derived_sentinel_booleans(result, flags):
    """Set ``is_master`` / ``is_slave`` / ``is_sdown`` / ``is_odown`` /
    ``is_sentinel`` / ``is_disconnected`` / ``is_master_down`` on
    ``result`` based on membership in the ``flags`` set.
    """
    for name, flag in _SENTINEL_DERIVED_BOOLEANS:
        result[name] = flag in flags

