
def _check_conn_kind(kind):
    """Check net_connections()'s `kind` parameter."""
    kinds = tuple(_common.conn_tmap)
    if kind not in kinds:
        msg = f"invalid kind argument {kind!r}; valid ones are: {kinds}"
        raise ValueError(msg)

