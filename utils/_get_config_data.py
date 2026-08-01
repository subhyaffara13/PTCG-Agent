
def _get_config_data(file_path: str, sections: tuple[str, ...]) -> dict[str, Any]:
    settings: dict[str, Any] = {}

    if file_path.endswith(".toml"):
        with open(file_path, "rb") as bin_config_file:
            config = tomllib.load(bin_config_file)
        for section in sections:
            config_section = config
            for key in section.split("."):
                config_section = config_section.get(key, {})
            settings.update(config_section)
    else:
        with open(file_path, encoding="utf-8") as config_file:
            if file_path.endswith(".editorconfig"):
                line = "\n"
                last_position = config_file.tell()
                while line:
                    line = config_file.readline()
                    if "[" in line:
                        config_file.seek(last_position)
                        break
                    last_position = config_file.tell()

            config = configparser.ConfigParser(strict=False)
            config.read_file(config_file)
        for section in sections:
            if section.startswith("*.{") and section.endswith("}"):
                extension = section[len("*.{") : -1]
                for config_key in config:
                    if (
                        config_key.startswith("*.{")
                        and config_key.endswith("}")
                        and extension
                        in (text.strip() for text in config_key[len("*.{") : -1].split(","))
                    ):
                        settings.update(config.items(config_key))

            elif config.has_section(section):
                settings.update(config.items(section))

    if settings:
        settings["source"] = file_path

        if file_path.endswith(".editorconfig"):
            indent_style = settings.pop("indent_style", "").strip()
            indent_size = settings.pop("indent_size", "").strip()
            if indent_size == "tab":
                indent_size = settings.pop("tab_width", "").strip()

            if indent_style == "space":
                settings["indent"] = " " * ((indent_size and int(indent_size)) or 4)

            elif indent_style == "tab":
                settings["indent"] = "\t" * ((indent_size and int(indent_size)) or 1)

            max_line_length = settings.pop("max_line_length", "").strip()
            if max_line_length and (max_line_length == "off" or max_line_length.isdigit()):
                settings["line_length"] = (
                    float("inf") if max_line_length == "off" else int(max_line_length)
                )
            settings = {
                key: value
                for key, value in settings.items()
                if key in _DEFAULT_SETTINGS or key.startswith(KNOWN_PREFIX)
            }

        for key, value in settings.items():
            existing_value_type = _get_str_to_type_converter(key)
            if existing_value_type is tuple:
                settings[key] = tuple(_as_list(value))
            elif existing_value_type is frozenset:
                settings[key] = frozenset(_as_list(settings.get(key)))  # type: ignore
            elif existing_value_type is bool:
                # Only some configuration formats support native boolean values.
                if not isinstance(value, bool):
                    value = _as_bool(value)
                settings[key] = value
            elif key.startswith(KNOWN_PREFIX):
                settings[key] = _abspaths(os.path.dirname(file_path), _as_list(value))
            elif key == "force_grid_wrap":
                try:
                    result = existing_value_type(value)
                except ValueError:  # backwards compatibility for true / false force grid wrap
                    result = 0 if value.lower().strip() == "false" else 2
                settings[key] = result
            elif key == "comment_prefix":
                settings[key] = str(value).strip("'").strip('"')
            else:
                settings[key] = existing_value_type(value)

    return settings

