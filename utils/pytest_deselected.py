
def pytest_deselected(items: Sequence[Item]) -> None:
    """Called for deselected test items, e.g. by keyword.

    Note that this hook has two integration aspects for plugins:

    - it can be *implemented* to be notified of deselected items
    - it must be *called* from :hook:`pytest_collection_modifyitems`
      implementations when items are deselected (to properly notify other plugins).

    May be called multiple times.

    :param items:
        The items.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook.
    """

