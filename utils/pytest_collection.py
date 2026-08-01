
def pytest_collection(session: Session) -> object | None:
    """Perform the collection phase for the given session.

    Stops at first non-None result, see :ref:`firstresult`.
    The return value is not used, but only stops further processing.

    The default collection phase is this (see individual hooks for full details):

    1. Starting from ``session`` as the initial collector:

      1. ``pytest_collectstart(collector)``
      2. ``report = pytest_make_collect_report(collector)``
      3. ``pytest_exception_interact(collector, call, report)`` if an interactive exception occurred
      4. For each collected node:

        1. If an item, ``pytest_itemcollected(item)``
        2. If a collector, recurse into it.

      5. ``pytest_collectreport(report)``

    2. ``pytest_collection_modifyitems(session, config, items)``

      1. ``pytest_deselected(items)`` for any deselected items (may be called multiple times)

    3. Set ``session.items`` to the list of collected items
    4. ``pytest_collection_finish(session)``
    5. Set ``session.testscollected`` to the number of collected items

    You can implement this hook to only perform some action before collection,
    for example the terminal plugin uses it to start displaying the collection
    counter (and returns `None`).

    :param session: The pytest session object.

    Use in conftest plugins
    =======================

    This hook is only called for :ref:`initial conftests <pluginorder>`.
    """


def pytest_collection(session: Session) -> None:
    session.perform_collect()


def pytest_collection(session: Session) -> Generator[None, object, object]:
    config = session.config
    with catch_warnings_for_item(
        config=config, ihook=config.hook, when="collect", item=None
    ):
        return (yield)


def pytest_collection(session: Session) -> None:
    # This hook is only called when test modules are collected
    # so for example not in the managing process of pytest-xdist
    # (which does not collect test modules).
    assertstate = session.config.stash.get(assertstate_key, None)
    if assertstate:
        if assertstate.hook is not None:
            assertstate.hook.set_session(session)

