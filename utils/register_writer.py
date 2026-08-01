
def register_writer(klass: ExcelWriter_t) -> None:
    """
    Add engine to the excel writer registry.io.excel.

    You must use this method to integrate with ``to_excel``.

    Parameters
    ----------
    klass : ExcelWriter
    """
    if not callable(klass):
        raise ValueError("Can only register callables as engines")
    engine_name = klass._engine
    _writers[engine_name] = klass

