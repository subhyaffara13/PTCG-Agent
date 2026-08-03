import sys
from pathlib import Path


def load_config_dict_from_file(
    filepath: Path,
) -> ConfigDict | None:
    """Load pytest configuration from the given file path, if supported.

    Return None if the file does not contain valid pytest configuration.
    """
    # Configuration from ini files are obtained from the [pytest] section, if present.
    if filepath.suffix == ".ini":
        iniconfig = _parse_ini_config(filepath)

        if "pytest" in iniconfig:
            return {
                k: ConfigValue(v, origin="file", mode="ini")
                for k, v in iniconfig["pytest"].items()
            }
        else:
            # "pytest.ini" files are always the source of configuration, even if empty.
            if filepath.name in {"pytest.ini", ".pytest.ini"}:
                return {}

    # '.cfg' files are considered if they contain a "[tool:pytest]" section.
    elif filepath.suffix == ".cfg":
        iniconfig = _parse_ini_config(filepath)

        if "tool:pytest" in iniconfig.sections:
            return {
                k: ConfigValue(v, origin="file", mode="ini")
                for k, v in iniconfig["tool:pytest"].items()
            }
        elif "pytest" in iniconfig.sections:
            # If a setup.cfg contains a "[pytest]" section, we raise a failure to indicate users that
            # plain "[pytest]" sections in setup.cfg files is no longer supported (#3086).
            fail(CFG_PYTEST_SECTION.format(filename="setup.cfg"), pytrace=False)

    # '.toml' files are considered if they contain a [tool.pytest] table (toml mode)
    # or [tool.pytest.ini_options] table (ini mode) for pyproject.toml,
    # or [pytest] table (toml mode) for pytest.toml/.pytest.toml.
    elif filepath.suffix == ".toml":
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            import tomli as tomllib

        toml_text = filepath.read_text(encoding="utf-8")
        try:
            config = tomllib.loads(toml_text)
        except tomllib.TOMLDecodeError as exc:
            raise UsageError(f"{filepath}: {exc}") from exc

        # pytest.toml and .pytest.toml use [pytest] table directly.
        if filepath.name in ("pytest.toml", ".pytest.toml"):
            pytest_config = config.get("pytest", {})
            if pytest_config:
                # TOML mode - preserve native TOML types.
                return {
                    k: ConfigValue(v, origin="file", mode="toml")
                    for k, v in pytest_config.items()
                }
            # "pytest.toml" files are always the source of configuration, even if empty.
            return {}

        # pyproject.toml uses [tool.pytest] or [tool.pytest.ini_options].
        else:
            tool_pytest = config.get("tool", {}).get("pytest", {})

            # Check for toml mode config: [tool.pytest] with content outside of ini_options.
            toml_config = {k: v for k, v in tool_pytest.items() if k != "ini_options"}
            # Check for ini mode config: [tool.pytest.ini_options].
            ini_config = tool_pytest.get("ini_options", None)

            if toml_config and ini_config:
                raise UsageError(
                    f"{filepath}: Cannot use both [tool.pytest] (native TOML types) and "
                    "[tool.pytest.ini_options] (string-based INI format) simultaneously. "
                    "Please use [tool.pytest] with native TOML types (recommended) "
                    "or [tool.pytest.ini_options] for backwards compatibility."
                )

            if toml_config:
                # TOML mode - preserve native TOML types.
                return {
                    k: ConfigValue(v, origin="file", mode="toml")
                    for k, v in toml_config.items()
                }

            elif ini_config is not None:
                # INI mode - TOML supports richer data types than INI files, but we need to
                # convert all scalar values to str for compatibility with the INI system.
                def make_scalar(v: object) -> str | list[str]:
                    return v if isinstance(v, list) else str(v)

                return {
                    k: ConfigValue(make_scalar(v), origin="file", mode="ini")
                    for k, v in ini_config.items()
                }

    return None

