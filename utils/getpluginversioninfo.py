
def getpluginversioninfo(config: Config) -> list[str]:
    lines = []
    plugininfo = config.pluginmanager.list_plugin_distinfo()
    if plugininfo:
        lines.append("registered third-party plugins:")
        for plugin, dist in plugininfo:
            loc = getattr(plugin, "__file__", repr(plugin))
            content = f"{dist.project_name}-{dist.version} at {loc}"
            lines.append("  " + content)
    return lines

