
def _parse_ini_config(path: Path) -> iniconfig.IniConfig:
    """Parse the given generic '.ini' file using legacy IniConfig parser, returning
    the parsed object.

    Raise UsageError if the file cannot be parsed.
    """
    try:
        return iniconfig.IniConfig(str(path))
    except iniconfig.ParseError as exc:
        raise UsageError(str(exc)) from exc

