
def _load_plugin(plugin: Plugin) -> LoadedPlugin:
    try:
        obj = plugin.entry_point.load()
    except Exception as e:
        raise FailedToLoadPlugin(plugin.package, e)

    if not callable(obj):
        err = TypeError("expected loaded plugin to be callable")
        raise FailedToLoadPlugin(plugin.package, err)

    return LoadedPlugin(plugin, obj, _parameters_for(obj))

