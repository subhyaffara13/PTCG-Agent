import os
import sys

def get_user_id() -> int | None:
    """Return the current process's real user id or None if it could not be
    determined.

    :return: The user id or None if it could not be determined.
    """
    # mypy follows the version and platform checking expectation of PEP 484:
    # https://mypy.readthedocs.io/en/stable/common_issues.html?highlight=platform#python-version-and-system-platform-checks
    # Containment checks are too complex for mypy v1.5.0 and cause failure.
    if sys.platform == "win32" or sys.platform == "emscripten":
        # win32 does not have a getuid() function.
        # Emscripten has a return 0 stub.
        return None
    else:
        # On other platforms, a return value of -1 is assumed to indicate that
        # the current process's real user id could not be determined.
        ERROR = -1
        uid = os.getuid()
        return uid if uid != ERROR else None

