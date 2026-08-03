from typing import Optional, Union

def _mb_to_bytes(max_request_size_mb: Optional[Union[int, float]]) -> Optional[int]:
    if max_request_size_mb is None:
        return None
    if max_request_size_mb <= 0:
        return None
    return int(max_request_size_mb * 1024 * 1024)

