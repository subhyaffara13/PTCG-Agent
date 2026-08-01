
def dict_subclass() -> type[dict]:
    """
    Fixture for a dictionary subclass.
    """

    class TestSubDict(dict):
        def __init__(self, *args, **kwargs) -> None:
            dict.__init__(self, *args, **kwargs)

    return TestSubDict

