
def pytest_addhooks(pluginmanager: PytestPluginManager) -> None:
    """Called at plugin registration time to allow adding new hooks via a call to
    :func:`pluginmanager.add_hookspecs(module_or_class, prefix) <pytest.PytestPluginManager.add_hookspecs>`.

    :param pluginmanager: The pytest plugin manager.

    .. note::
        This hook is incompatible with hook wrappers.

    Use in conftest plugins
    =======================

    If a conftest plugin implements this hook, it will be called immediately
    when the conftest is registered.
    """

