
def pytest_sessionfinish(
    session: Session,
    exitstatus: int | ExitCode,
) -> None:
    """Called after whole test run finished, right before returning the exit status to the system.

    :param session: The pytest session object.
    :param exitstatus: The status which pytest will return to the system.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook.
    """


def pytest_sessionfinish(session: Session) -> None:
    session._setupstate.teardown_exact(None)


def pytest_sessionfinish(session: Session) -> None:
    if not session.config.getoption("stepwise"):
        assert session.config.cache is not None
        if hasattr(session.config, "workerinput"):
            # Do not update cache if this process is a xdist worker to prevent
            # race conditions (#10641).
            return


def pytest_sessionfinish(session, exitstatus: int | ExitCode):
    """After each session, remove base directory if all the tests passed,
    the policy is "failed", and the basetemp is not specified by a user.
    """
    tmp_path_factory: TempPathFactory = session.config._tmp_path_factory
    basetemp = tmp_path_factory._basetemp
    if basetemp is None:
        return

    policy = tmp_path_factory._retention_policy
    if (
        exitstatus == 0
        and policy == "failed"
        and tmp_path_factory._given_basetemp is None
    ):
        if basetemp.is_dir():
            # We do a "best effort" to remove files, but it might not be possible due to some leaked resource,
            # permissions, etc, in which case we ignore it.
            rmtree(basetemp, ignore_errors=True)

    # Remove dead symlinks.
    if basetemp.is_dir():
        cleanup_dead_symlinks(basetemp)

    # Run the numbered dirs and lock file cleanups registered on the ExitStack.
    tmp_path_factory._exit_stack.close()


def pytest_sessionfinish(session: Session) -> Generator[None]:
    config = session.config
    with catch_warnings_for_item(
        config=config, ihook=config.hook, when="config", item=None
    ):
        return (yield)


def pytest_sessionfinish(session: Session) -> None:
    assertstate = session.config.stash.get(assertstate_key, None)
    if assertstate:
        if assertstate.hook is not None:
            assertstate.hook.set_session(None)

