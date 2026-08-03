import json
import os

def read_status(status_file: str) -> dict[str, object]:
    """Read status file.

    Raise BadStatus if the status file doesn't exist or contains
    invalid JSON or the JSON is not a dict.
    """
    if not os.path.isfile(status_file):
        raise BadStatus("No status file found")
    with open(status_file) as f:
        try:
            data = json.load(f)
        except Exception as e:
            raise BadStatus(f"Malformed status file: {str(e)}") from e
    if not isinstance(data, dict):
        raise BadStatus(f"Invalid status file (not a dict): {data}")
    return data

