
def pytest_sessionstart(session):
    available_mem = session.config.getoption('available_memory')
    if available_mem is not None:
        os.environ['NPY_AVAILABLE_MEM'] = available_mem


def pytest_sessionstart(session):
    import doctest
    import inspect

    # https://github.com/pandas-dev/pandas/pull/62988
    # When we modify the __module__ of a class, the __module__ on the methods
    # of that class do not change. When these two disagree, doctests would not
    # typically run. We hack `DocTestFinder` to avoid this.
    orig = doctest.DocTestFinder._from_module  # type: ignore[attr-defined]

    def _from_module(self, module, object):
        # When . is in __qualname__, object is a method of a class.
        if inspect.isfunction(object) and "." in object.__qualname__:
            # We only get here when the class that the method is on is from the
            # appropriate module. So ignore checking the __module__ of the method
            # itself and run the doctest.
            return True
        return orig(self, module, object)

    doctest.DocTestFinder._from_module = _from_module  # type: ignore[attr-defined]


def pytest_sessionstart(session: Session) -> None:
    session._fixturemanager = FixtureManager(session)


def pytest_sessionstart(session: Session) -> None:
    """Called after the ``Session`` object has been created and before performing collection
    and entering the run test loop.

    :param session: The pytest session object.

    Use in conftest plugins
    =======================

    This hook is only called for :ref:`initial conftests <pluginorder>`.
    """


def pytest_sessionstart(session: Session) -> None:
    session._setupstate = SetupState()


def pytest_sessionstart(session: Any) -> None:
    # Clean up directory where mypyc tests write intermediate files on failure
    # to avoid any confusion between test runs
    if os.path.isdir(mypyc_output_dir):
        shutil.rmtree(mypyc_output_dir)

