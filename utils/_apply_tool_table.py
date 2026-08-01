
def _apply_tool_table(dist: Distribution, config: dict, filename: StrPath):
    tool_table = config.get("tool", {}).get("setuptools", {})
    if not tool_table:
        return  # short-circuit

    if "license-files" in tool_table:
        if "license-files" in config.get("project", {}):
            # https://github.com/pypa/setuptools/pull/4837#discussion_r2004983349
            raise InvalidConfigError(
                "'project.license-files' is defined already. "
                "Remove 'tool.setuptools.license-files'."
            )

        pypa_guides = "guides/writing-pyproject-toml/#license-files"
        SetuptoolsDeprecationWarning.emit(
            "'tool.setuptools.license-files' is deprecated in favor of "
            "'project.license-files' (available on setuptools>=77.0.0).",
            see_url=f"https://packaging.python.org/en/latest/{pypa_guides}",
            due_date=(2027, 2, 18),  # Warning introduced on 2025-02-18
        )

    for field, value in tool_table.items():
        norm_key = json_compatible_key(field)

        if norm_key in TOOL_TABLE_REMOVALS:
            suggestion = cleandoc(TOOL_TABLE_REMOVALS[norm_key])
            msg = f"""
            The parameter `tool.setuptools.{field}` was long deprecated
            and has been removed from `pyproject.toml`.
            """
            raise RemovedConfigError("\n".join([cleandoc(msg), suggestion]))

        norm_key = TOOL_TABLE_RENAMES.get(norm_key, norm_key)
        corresp = TOOL_TABLE_CORRESPONDENCE.get(norm_key, norm_key)
        if callable(corresp):
            corresp(dist, value)
        else:
            _set_config(dist, corresp, value)

    _copy_command_options(config, dist, filename)

