
def wait_until_pending_futures_and_users_flushed(timeout: int = 20) -> None:
    """
    The RRef protocol holds forkIds of rrefs in a map until those forks are
    confirmed by the owner. The message confirming the fork may arrive after
    our tests check whether this map is empty, which leads to failures and
    flaky tests. to_here also does not guarantee that we have finished
    processind the owner's confirmation message for the RRef. This function
    loops until the map is empty, which means the messages have been received
    as processed. Call this function before asserting the map returned by
    _get_debug_info is empty.
    """
    start = time.time()
    while True:
        debug_info = _rref_context_get_debug_info()
        num_pending_futures = int(debug_info["num_pending_futures"])
        num_pending_users = int(debug_info["num_pending_users"])
        if num_pending_futures == 0 and num_pending_users == 0:
            break
        time.sleep(0.1)
        if time.time() - start > timeout:
            raise ValueError(
                f"Timed out waiting to flush pending futures and users, "
                f"had {num_pending_futures} pending futures and {num_pending_users} pending users"
            )

