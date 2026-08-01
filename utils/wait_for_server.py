
def wait_for_server(status_file: str, timeout: float = 5.0) -> None:
    """Wait until the server is up.

    Exit if it doesn't happen within the timeout.
    """
    endtime = time.time() + timeout
    while time.time() < endtime:
        try:
            data = read_status(status_file)
        except BadStatus:
            # If the file isn't there yet, retry later.
            time.sleep(0.1)
            continue
        # If the file's content is bogus or the process is dead, fail.
        check_status(data)
        print("Daemon started")
        return
    fail("Timed out waiting for daemon to start")

