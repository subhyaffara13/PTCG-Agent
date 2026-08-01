
def load_plugins(
    options: Options, errors: Errors, stdout: TextIO, extra_plugins: Sequence[Plugin]
) -> tuple[Plugin, dict[str, str]]:
    """Load all configured plugins.

    Return a plugin that encapsulates all plugins chained together. Always
    at least include the default plugin (it's last in the chain).
    The second return value is a snapshot of versions/hashes of loaded user
    plugins (for cache validation).
    """
    custom_plugins, snapshot = load_plugins_from_config(options, errors, stdout)

    custom_plugins += extra_plugins

    default_plugin: Plugin = DefaultPlugin(options)
    if not custom_plugins:
        return default_plugin, snapshot

    # Custom plugins take precedence over the default plugin.
    return ChainedPlugin(options, custom_plugins + [default_plugin]), snapshot


def load_plugins(
    plugins: list[Plugin],
    opts: PluginOptions,
) -> Plugins:
    """Load and classify all flake8 plugins.

    - first: extends ``sys.path`` with ``paths`` (to import local plugins)
    - next: converts the ``Plugin``s to ``LoadedPlugins``
    - finally: classifies plugins into their specific types
    """
    return _classify_plugins(_import_plugins(plugins, opts), opts)

