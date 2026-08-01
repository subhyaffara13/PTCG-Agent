
def _cleanup_connections() -> None:
    with _all_connections_lock:
        for con in list(_all_connections):
            with suppress(Exception):
                con.close()
        _all_connections.clear()

