
def _ignore_errors(ignore_option_errors: bool):
    if not ignore_option_errors:
        yield
        return

    try:
        yield
    except Exception as ex:
        _logger.debug(f"ignored error: {ex.__class__.__name__} - {ex}")

