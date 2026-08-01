
def pytest_runtestloop(session: Session) -> object | None:
    """Perform the main runtest loop (after collection finished).

    The default hook implementation performs the runtest protocol for all items
    collected in the session (``session.items``), unless the collection failed
    or the ``collectonly`` pytest option is set.

    If at any point :py:func:`pytest.exit` is called, the loop is
    terminated immediately.

    If at any point ``session.shouldfail`` or ``session.shouldstop`` are set, the
    loop is terminated after the runtest protocol for the current item is finished.

    :param session: The pytest session object.

    Stops at first non-None result, see :ref:`firstresult`.
    The return value is not used, but only stops further processing.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook.
    """


def pytest_runtestloop(session: Session) -> bool:
    if session.testsfailed and not session.config.option.continue_on_collection_errors:
        raise session.Interrupted(
            f"{session.testsfailed} error{'s' if session.testsfailed != 1 else ''} during collection"
        )

    if session.config.option.collectonly:
        return True

    for i, item in enumerate(session.items):
        nextitem = session.items[i + 1] if i + 1 < len(session.items) else None
        item.config.hook.pytest_runtest_protocol(item=item, nextitem=nextitem)
        if session.shouldfail:
            raise session.Failed(session.shouldfail)
        if session.shouldstop:
            raise session.Interrupted(session.shouldstop)
    return True

