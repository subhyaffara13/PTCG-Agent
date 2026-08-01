
def grok_environment_error(exc: object, prefix: str = "error: ") -> str:
    # Function kept for backward compatibility.
    # Used to try clever things with EnvironmentErrors,
    # but nowadays str(exception) produces good messages.
    return prefix + str(exc)

