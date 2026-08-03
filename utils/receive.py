import json
from typing import Any

def receive(connection: IPCBase) -> Any:
    """Receive single JSON data frame from a connection.

    Raise OSError if the data received is not valid JSON or if it is
    not a dict.
    """
    bdata = connection.read()
    if not bdata:
        raise OSError("No data received")
    try:
        data = json.loads(bdata)
    except Exception as e:
        raise OSError("Data received is not valid JSON") from e
    if not isinstance(data, dict):
        raise OSError(f"Data received is not a dict ({type(data)})")
    return data


def receive(connection: IPCBase) -> ReadBuffer:
    """Receive single encoded IPCMessage frame from a connection.

    Raise OSError if the data received is not valid.
    """
    bdata = connection.read_bytes()
    if not bdata:
        raise OSError("No data received")
    return ReadBuffer(bdata)

