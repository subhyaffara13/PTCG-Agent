
def destructure_overrides(toml_data: dict[str, Any]) -> dict[str, Any]:
    """Take the new [[tool.mypy.overrides]] section array in the pyproject.toml file,
    and convert it back to a flatter structure that the existing config_parser can handle.

    E.g. the following pyproject.toml file:

        [[tool.mypy.overrides]]
        module = [
            "a.b",
            "b.*"
        ]
        disallow_untyped_defs = true

        [[tool.mypy.overrides]]
        module = 'c'
        disallow_untyped_defs = false

    Would map to the following config dict that it would have gotten from parsing an equivalent
    ini file:

        {
            "mypy-a.b": {
                disallow_untyped_defs = true,
            },
            "mypy-b.*": {
                disallow_untyped_defs = true,
            },
            "mypy-c": {
                disallow_untyped_defs: false,
            },
        }
    """
    if "overrides" not in toml_data["mypy"]:
        return toml_data

    if not isinstance(toml_data["mypy"]["overrides"], list):
        raise ConfigTOMLValueError(
            "tool.mypy.overrides sections must be an array. Please make "
            "sure you are using double brackets like so: [[tool.mypy.overrides]]"
        )

    result = toml_data.copy()
    for override in result["mypy"]["overrides"]:
        if "module" not in override:
            raise ConfigTOMLValueError(
                "toml config file contains a [[tool.mypy.overrides]] "
                "section, but no module to override was specified."
            )

        if isinstance(override["module"], str):
            modules = [override["module"]]
        elif isinstance(override["module"], list):
            modules = override["module"]
        else:
            raise ConfigTOMLValueError(
                "toml config file contains a [[tool.mypy.overrides]] "
                "section with a module value that is not a string or a list of "
                "strings"
            )

        for module in modules:
            module_overrides = override.copy()
            del module_overrides["module"]
            old_config_name = f"mypy-{module}"
            if old_config_name not in result:
                result[old_config_name] = module_overrides
            else:
                for new_key, new_value in module_overrides.items():
                    if (
                        new_key in result[old_config_name]
                        and result[old_config_name][new_key] != new_value
                    ):
                        raise ConfigTOMLValueError(
                            "toml config file contains "
                            "[[tool.mypy.overrides]] sections with conflicting "
                            f"values. Module '{module}' has two different values for '{new_key}'"
                        )
                    result[old_config_name][new_key] = new_value

    del result["mypy"]["overrides"]
    return result

