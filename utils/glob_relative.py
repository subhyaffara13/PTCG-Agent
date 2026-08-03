import os

def glob_relative(
    patterns: Iterable[str], root_dir: StrPath | None = None
) -> list[str]:
    """Expand the list of glob patterns, but preserving relative paths.

    :param list[str] patterns: List of glob patterns
    :param str root_dir: Path to which globs should be relative
                         (current directory by default)
    :rtype: list
    """
    glob_characters = {'*', '?', '[', ']', '{', '}'}
    expanded_values = []
    root_dir = root_dir or os.getcwd()
    for value in patterns:
        # Has globby characters?
        if any(char in value for char in glob_characters):
            # then expand the glob pattern while keeping paths *relative*:
            glob_path = os.path.abspath(os.path.join(root_dir, value))
            expanded_values.extend(
                sorted(
                    os.path.relpath(path, root_dir).replace(os.sep, "/")
                    for path in iglob(glob_path, recursive=True)
                )
            )

        else:
            # take the value as-is
            path = os.path.relpath(value, root_dir).replace(os.sep, "/")
            expanded_values.append(path)

    return expanded_values

