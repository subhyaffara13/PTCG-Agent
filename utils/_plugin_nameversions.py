
def _plugin_nameversions(plugininfo) -> list[str]:
    values: list[str] = []
    for plugin, dist in plugininfo:
        # Gets us name and version!
        name = f"{dist.project_name}-{dist.version}"
        # Questionable convenience, but it keeps things short.
        if name.startswith("pytest-"):
            name = name[7:]
        # We decided to print python package names they can have more than one plugin.
        if name not in values:
            values.append(name)
    return values

