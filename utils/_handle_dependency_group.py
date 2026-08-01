
def _handle_dependency_group(
    option: Option, opt: str, value: str, parser: OptionParser
) -> None:
    """
    Process a value provided for the --group option.

    Splits on the rightmost ":", and validates that the path (if present) ends
    in `pyproject.toml`. Defaults the path to `pyproject.toml` when one is not given.

    `:` cannot appear in dependency group names, so this is a safe and simple parse.

    This is an optparse.Option callback for the dependency_groups option.
    """
    path, sep, groupname = value.rpartition(":")
    if not sep:
        path = "pyproject.toml"
    else:
        # check for 'pyproject.toml' filenames using pathlib
        if pathlib.PurePath(path).name != "pyproject.toml":
            msg = "group paths use 'pyproject.toml' filenames"
            raise_option_error(parser, option=option, msg=msg)

    parser.values.dependency_groups.append((path, groupname))

