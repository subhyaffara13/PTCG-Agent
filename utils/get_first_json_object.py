import json
from typing import Optional, Union

def get_first_json_object(file_source: Union[bytes, BinaryIO]) -> Optional[dict]:
    try:
        if isinstance(file_source, (bytes, bytearray)):
            newline = file_source.find(b"\n")
            raw = file_source if newline == -1 else file_source[:newline]
            first_line = raw.decode("utf-8")
        else:
            file_source.seek(0)
            first_line = file_source.readline().decode("utf-8")
            file_source.seek(0)
        return json.loads(first_line.strip())
    except (json.JSONDecodeError, UnicodeDecodeError, OSError, ValueError):
        return None

