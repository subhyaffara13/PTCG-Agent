from typing import Any

def check_status(data: dict[str, Any]) -> tuple[int, str]:
    """Check if the process is alive.

    Return (pid, connection_name) on success.

    Raise BadStatus if something's wrong.
    """
    if "pid" not in data:
        raise BadStatus("Invalid status file (no pid field)")
    pid = data["pid"]
    if not isinstance(pid, int):
        raise BadStatus("pid field is not an int")
    if not alive(pid):
        raise BadStatus("Daemon has died")
    if "connection_name" not in data:
        raise BadStatus("Invalid status file (no connection_name field)")
    connection_name = data["connection_name"]
    if not isinstance(connection_name, str):
        raise BadStatus("connection_name field is not a string")
    return pid, connection_name

