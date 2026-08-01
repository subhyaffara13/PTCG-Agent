
def console_main() -> int:
    """The CLI entry point of pytest.

    .. deprecated:: 9.1
        This function is slated for removal in pytest 10.
        It is not meant for programmable use; use :func:`pytest.main` instead.
    """
    import warnings

    from _pytest.deprecated import CONSOLE_MAIN

    warnings.warn(CONSOLE_MAIN, stacklevel=2)
    return _console_main()

