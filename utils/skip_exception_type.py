
def skip_exception_type(exc_type):
    try:
        yield
    except exc_type as e:
        raise unittest.SkipTest(f"not implemented: {e}") from e

