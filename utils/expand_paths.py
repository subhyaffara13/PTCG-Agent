
def expand_paths(
    *,
    paths: Sequence[str],
    stdin_display_name: str,
    filename_patterns: Sequence[str],
    exclude: Sequence[str],
) -> Generator[str]:
    """Expand out ``paths`` from commandline to the lintable files."""
    if not paths:
        paths = ["."]

    def is_excluded(arg: str) -> bool:
        if arg == "-":
            # if the stdin_display_name is the default, always include it
            if stdin_display_name == "stdin":
                return False
            arg = stdin_display_name

        return utils.matches_filename(
            arg,
            patterns=exclude,
            log_message='"%(path)s" has %(whether)sbeen excluded',
            logger=LOG,
        )

    return (
        filename
        for path in paths
        for filename in _filenames_from(path, predicate=is_excluded)
        if (
            # always lint `-`
            filename == "-"
            # always lint explicitly passed (even if not matching filter)
            or path == filename
            # otherwise, check the file against filtered patterns
            or utils.fnmatch(filename, filename_patterns)
        )
    )

