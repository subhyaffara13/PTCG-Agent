
def _check_full_rank(store, world_size, timeout):
    try:
        barrier(store, world_size, key_prefix=_TCP_STORE_INIT, barrier_timeout=timeout)
    except RuntimeError as e:
        if str(e) == _SOCKET_TIMEOUT:
            raise TimeoutError(
                f"timed out waiting for all {world_size} members to join"
            ) from e
        else:
            raise

