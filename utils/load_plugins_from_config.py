
def load_plugins_from_config(
    options: Options, errors: Errors, stdout: TextIO
) -> tuple[list[Plugin], dict[str, str]]:
    """Load all configured plugins.

    Return a list of all the loaded plugins from the config file.
    The second return value is a snapshot of versions/hashes of loaded user
    plugins (for cache validation).
    """
    import importlib

    snapshot: dict[str, str] = {}

    if not options.config_file:
        return [], snapshot

    line = find_config_file_line_number(options.config_file, "mypy", "plugins")
    if line == -1:
        line = 1  # We need to pick some line number that doesn't look too confusing

    def plugin_error(message: str) -> NoReturn:
        errors.report(line, 0, message)
        errors.raise_error(use_stdout=False)

    custom_plugins: list[Plugin] = []
    errors.set_file(options.config_file, None, options)
    for plugin_path in options.plugins:
        func_name = "plugin"
        plugin_dir: str | None = None
        if ":" in os.path.basename(plugin_path):
            plugin_path, func_name = plugin_path.rsplit(":", 1)
        if plugin_path.endswith(".py"):
            # Plugin paths can be relative to the config file location.
            plugin_path = os_path_join(os.path.dirname(options.config_file), plugin_path)
            if not os.path.isfile(plugin_path):
                plugin_error(f'Can\'t find plugin "{plugin_path}"')
            # Use an absolute path to avoid populating the cache entry
            # for 'tmp' during tests, since it will be different in
            # different tests.
            plugin_dir = os.path.abspath(os.path.dirname(plugin_path))
            fnam = os.path.basename(plugin_path)
            module_name = fnam[:-3]
            sys.path.insert(0, plugin_dir)
        elif re.search(r"[\\/]", plugin_path):
            fnam = os.path.basename(plugin_path)
            plugin_error(f'Plugin "{fnam}" does not have a .py extension')
        else:
            module_name = plugin_path

        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            plugin_error(f'Error importing plugin "{plugin_path}": {exc}')
        finally:
            if plugin_dir is not None:
                assert sys.path[0] == plugin_dir
                del sys.path[0]

        if not hasattr(module, func_name):
            plugin_error(
                'Plugin "{}" does not define entry point function "{}"'.format(
                    plugin_path, func_name
                )
            )

        try:
            plugin_type = getattr(module, func_name)(__version__)
        except Exception:
            print(f"Error calling the plugin(version) entry point of {plugin_path}\n", file=stdout)
            raise  # Propagate to display traceback

        if not isinstance(plugin_type, type):
            plugin_error(
                'Type object expected as the return value of "plugin"; got {!r} (in {})'.format(
                    plugin_type, plugin_path
                )
            )
        if not issubclass(plugin_type, Plugin):
            plugin_error(
                'Return value of "plugin" must be a subclass of "mypy.plugin.Plugin" '
                "(in {})".format(plugin_path)
            )
        try:
            custom_plugins.append(plugin_type(options))
            snapshot[module_name] = take_module_snapshot(module)
        except Exception:
            print(f"Error constructing plugin instance of {plugin_type.__name__}\n", file=stdout)
            raise  # Propagate to display traceback

    return custom_plugins, snapshot

