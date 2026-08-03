from pathlib import Path


def pytest_report_collectionfinish(  # type: ignore[empty-body]
    config: Config,
    start_path: Path,
    items: Sequence[Item],
) -> str | list[str]:
    """Return a string or list of strings to be displayed after collection
    has finished successfully.

    These strings will be displayed after the standard "collected X items" message.

    .. versionadded:: 3.2

    :param config: The pytest config object.
    :param start_path: The starting dir.
    :type start_path: pathlib.Path
    :param items: List of pytest items that are going to be executed; this list should not be modified.

    .. note::

        Lines returned by a plugin are displayed before those of plugins which
        ran before it.
        If you want to have your line(s) displayed first, use
        :ref:`trylast=True <plugin-hookorder>`.

    .. versionchanged:: 7.0.0
        The ``start_path`` parameter was added as a :class:`pathlib.Path`
        equivalent of the ``startdir`` parameter. The ``startdir`` parameter
        has been deprecated and removed in pytest 9.0.0.

    Use in conftest plugins
    =======================

    Any conftest plugin can implement this hook.
    """

