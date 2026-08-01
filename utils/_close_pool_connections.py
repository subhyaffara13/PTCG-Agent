
def _close_pool_connections(pool: queue.LifoQueue[typing.Any]) -> None:
    """Drains a queue of connections and closes each one."""
    try:
        while True:
            conn = pool.get(block=False)
            if conn:
                conn.close()
    except queue.Empty:
        pass  # Done.


def _close_pool_connections(pool: queue.LifoQueue[typing.Any]) -> None:
    """Drains a queue of connections and closes each one."""
    try:
        while True:
            conn = pool.get(block=False)
            if conn:
                conn.close()
    except queue.Empty:
        pass  # Done.

