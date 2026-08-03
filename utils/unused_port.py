from typing import Callable

def unused_port(aiohttp_unused_port: Callable[[], int]) -> Callable[[], int]:
    warnings.warn(
        "Deprecated, use aiohttp_unused_port fixture instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return aiohttp_unused_port


def unused_port() -> int:
    """Return a port that is unused on the current host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return cast(int, s.getsockname()[1])

