
def is_ssl_error(error: Exception | None = None) -> bool:
    """Checks if the given error (or the current one) is an SSL error."""
    if error is None:
        error = t.cast(Exception, sys.exc_info()[1])
    return isinstance(error, ssl.SSLError)

