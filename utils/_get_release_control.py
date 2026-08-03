from typing import Any

def _get_release_control(values: Values, option: Option) -> Any:
    """Get a release_control object."""
    return getattr(values, option.dest)

