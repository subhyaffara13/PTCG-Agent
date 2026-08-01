
def req_error_context(req_description: str) -> Generator[None, None, None]:
    try:
        yield
    except InstallationError as e:
        message = f"For req: {req_description}. {e.args[0]}"
        raise InstallationError(message) from e

