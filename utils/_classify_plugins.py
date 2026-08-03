import itertools

def _classify_plugins(
    plugins: list[LoadedPlugin],
    opts: PluginOptions,
) -> Plugins:
    tree = []
    logical_line = []
    physical_line = []
    reporters = {}
    disabled = []

    for loaded in plugins:
        if (
            getattr(loaded.obj, "off_by_default", False)
            and loaded.plugin.entry_point.name not in opts.enable_extensions
        ):
            disabled.append(loaded)
        elif loaded.plugin.entry_point.group == "flake8.report":
            reporters[loaded.entry_name] = loaded
        elif "tree" in loaded.parameters:
            tree.append(loaded)
        elif "logical_line" in loaded.parameters:
            logical_line.append(loaded)
        elif "physical_line" in loaded.parameters:
            physical_line.append(loaded)
        else:
            raise NotImplementedError(f"what plugin type? {loaded}")

    for loaded in itertools.chain(tree, logical_line, physical_line):
        if not VALID_CODE_PREFIX.match(loaded.entry_name):
            raise ExecutionError(
                f"plugin code for `{loaded.display_name}` does not match "
                f"{VALID_CODE_PREFIX.pattern}"
            )

    return Plugins(
        checkers=Checkers(
            tree=tree,
            logical_line=logical_line,
            physical_line=physical_line,
        ),
        reporters=reporters,
        disabled=disabled,
    )

