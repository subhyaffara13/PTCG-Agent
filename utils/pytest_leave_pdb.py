
def pytest_leave_pdb(config: Config, pdb: pdb.Pdb) -> None:
    """Called when leaving pdb (e.g. with continue after pdb.set_trace()).

    Can be used by plugins to take special action just after the python
    debugger leaves interactive mode.

    :param config: The pytest config object.
    :param pdb: The Pdb instance.

    Use in conftest plugins
    =======================

    Any conftest plugin can implement this hook.
    """

