
def pytest_enter_pdb() -> None:
    """Cancel any traceback dumping due to timeout before entering pdb."""
    import faulthandler

    faulthandler.cancel_dump_traceback_later()


def pytest_enter_pdb(config: Config, pdb: pdb.Pdb) -> None:
    """Called upon pdb.set_trace().

    Can be used by plugins to take special action just before the python
    debugger enters interactive mode.

    :param config: The pytest config object.
    :param pdb: The Pdb instance.

    Use in conftest plugins
    =======================

    Any conftest plugin can implement this hook.
    """

