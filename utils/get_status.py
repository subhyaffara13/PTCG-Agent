
def get_status(status_file: str) -> tuple[int, str]:
    """Read status file and check if the process is alive.

    Return (pid, connection_name) on success.

    Raise BadStatus if something's wrong.
    """
    data = read_status(status_file)
    return check_status(data)

