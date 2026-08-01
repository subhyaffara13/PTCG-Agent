
def _parse_individual_file(
    config_file: str, stderr: TextIO | None = None
) -> tuple[MutableMapping[str, Any], dict[str, _INI_PARSER_CALLABLE], str] | None:

    if not os.path.exists(config_file):
        return None

    parser: MutableMapping[str, Any]
    try:
        if is_toml(config_file):
            with open(config_file, "rb") as f:
                toml_data = tomllib.load(f)
            # Filter down to just mypy relevant toml keys
            toml_data = toml_data.get("tool", {})
            if "mypy" not in toml_data:
                return None
            toml_data = {"mypy": toml_data["mypy"]}
            parser = destructure_overrides(toml_data)
            config_types = toml_config_types
        else:
            parser = configparser.RawConfigParser()
            parser.read(config_file)
            config_types = ini_config_types

    except (tomllib.TOMLDecodeError, configparser.Error, ConfigTOMLValueError) as err:
        print(f"{config_file}: {err}", file=stderr)
        return None

    if os.path.basename(config_file) in defaults.SHARED_CONFIG_NAMES and "mypy" not in parser:
        return None

    return parser, config_types, config_file

