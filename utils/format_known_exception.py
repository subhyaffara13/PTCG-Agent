
def format_known_exception(error: Exception) -> str | None:
    for exc_type, formatter in CLI_ERROR_MAPPINGS.items():
        if isinstance(error, exc_type):
            return formatter(error)
    return None

