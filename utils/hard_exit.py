import os
import sys

def hard_exit(status: int = 0) -> None:
    """Kill the current process without fully cleaning up.

    This can be quite a bit faster than a normal exit() since objects are not freed.
    """
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(status)

