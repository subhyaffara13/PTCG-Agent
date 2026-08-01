
def enable_warning(warning):
    warnings.simplefilter("always", warning)
    try:
        yield
    finally:
        # Reset it to default value, so it will take
        # into account the values from the -W flag.
        warnings.simplefilter("default", warning)

