import os
from typing import Union

def get_file_modtime(path: Union[bytes, str, "os.PathLike[Text]"]) -> Text:
    """Returns ISO formatted file modification time in local system timezone"""
    return (
        datetime.fromtimestamp(os.stat(path).st_mtime, timezone.utc)
        .astimezone()
        .isoformat()
    )

