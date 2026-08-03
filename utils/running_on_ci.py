import os

def running_on_ci() -> bool:
    """Check if we're currently running on a CI system."""
    # Only enable CI mode if one of these env variables is defined and non-empty.
    # Note: review `regendoc` tox env in case this list is changed.
    env_vars = ["CI", "BUILD_NUMBER"]
    return any(os.environ.get(var) for var in env_vars)

