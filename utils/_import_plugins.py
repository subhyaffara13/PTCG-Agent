
def _import_plugins(
    plugins: list[Plugin],
    opts: PluginOptions,
) -> list[LoadedPlugin]:
    sys.path.extend(opts.local_plugin_paths)
    return [_load_plugin(p) for p in plugins]

