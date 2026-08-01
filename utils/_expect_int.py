
def _expect_int(value, msg=None):
    try:
        return int(value)
    except ValueError as e:
        if msg is None:
            msg = "Expected an int, got %s"
        raise ValueError(msg % value) from e

