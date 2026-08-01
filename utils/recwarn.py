
def recwarn() -> Generator[WarningsRecorder]:
    """Return a :class:`WarningsRecorder` instance that records all warnings emitted by test functions.

    See :ref:`warnings` for information on warning categories.
    """
    wrec = WarningsRecorder(_ispytest=True)
    with wrec:
        warnings.simplefilter("default")
        yield wrec

