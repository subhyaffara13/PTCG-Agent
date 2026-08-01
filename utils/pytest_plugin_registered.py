
def pytest_plugin_registered(
    plugin: _PluggyPlugin,
    plugin_name: str,
    manager: PytestPluginManager,
) -> None:
    """A new pytest plugin got registered.

    :param plugin: The plugin module or instance.
    :param plugin_name: The name by which the plugin is registered.
    :param manager: The pytest plugin manager.

    .. note::
        This hook is incompatible with hook wrappers.

    Use in conftest plugins
    =======================

    If a conftest plugin implements this hook, it will be called immediately
    when the conftest is registered, once for each plugin registered thus far
    (including itself!), and for all plugins thereafter when they are
    registered.
    """


def pytest_plugin_registered(plugin: object, manager: PytestPluginManager) -> None:
    # pytester is not loaded by default and is commonly loaded from a conftest,
    # so checking for it in `pytest_configure` is not enough.
    is_pytester = plugin is manager.get_plugin("pytester")
    if is_pytester and not manager.is_registered(LegacyTestdirPlugin):
        manager.register(LegacyTestdirPlugin, "legacypath-pytester")

