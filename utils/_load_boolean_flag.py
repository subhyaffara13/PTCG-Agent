import os

def _load_boolean_flag(
    name: str,
    *,
    this_will: str,
    deprecated: bool = False,
    default: bool = False,
) -> bool:
    """Load a boolean flag from environment variable.

    Args:
        name: The name of the environment variable.
        this_will: A string that describes what this flag will do.
        deprecated: Whether this flag is deprecated.
        default: The default value if envvar not defined.
    """
    undefined = os.getenv(name) is None
    state = os.getenv(name) == "1"
    if state:
        if deprecated:
            logger.error(
                "Experimental flag %s is deprecated. Please remove it from your environment.",
                name,
            )
        else:
            logger.warning(
                "Experimental flag %s is enabled. This will %s.", name, this_will
            )
    if undefined:
        state = default
    return state

