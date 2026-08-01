
def register_network_debug_plugin(config) -> None:
    """Register the network debug pytest plugin. Single entry point for conftest.py."""
    config.pluginmanager.register(NetworkDebugPlugin(), "network_debug")

