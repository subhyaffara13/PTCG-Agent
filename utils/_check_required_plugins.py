
def _check_required_plugins(
    plugins: list[Plugin],
    expected: frozenset[str],
) -> None:
    plugin_names = {
        utils.normalize_pypi_name(plugin.package) for plugin in plugins
    }
    expected_names = {utils.normalize_pypi_name(name) for name in expected}
    missing_plugins = expected_names - plugin_names

    if missing_plugins:
        raise ExecutionError(
            f"required plugins were not installed!\n"
            f"- installed: {', '.join(sorted(plugin_names))}\n"
            f"- expected: {', '.join(sorted(expected_names))}\n"
            f"- missing: {', '.join(sorted(missing_plugins))}"
        )

