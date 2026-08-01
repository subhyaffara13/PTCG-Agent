
def _warn_if_invalid(nb, version):
    """Log validation errors, if there are any."""
    from nbformat import ValidationError, validate

    try:
        validate(nb, version=version)
    except ValidationError as e:
        get_logger().error("Notebook JSON is not valid v%i: %s", version, e)

