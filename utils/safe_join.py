
def safe_join(t: Type, s: Type) -> Type:
    # This is a temporary solution to prevent crashes in combine_similar_callables() etc.,
    # until relevant TODOs on handling arg_kinds will be addressed there.
    if not isinstance(t, UnpackType) and not isinstance(s, UnpackType):
        return join_types(t, s)
    if isinstance(t, UnpackType) and isinstance(s, UnpackType):
        return UnpackType(join_types(t.type, s.type))
    return object_or_any_from_type(get_proper_type(t))


def safe_join(directory: str, *untrusted: str) -> str | None:
    """Safely join zero or more untrusted path components to a trusted base
    directory to avoid escaping the base directory.

    The untrusted path is assumed to be from/for a URL, such as for serving
    files. Therefore, it should only use the forward slash ``/`` path separator,
    and will be joined using that separator. On Windows, the backslash ``\\``
    separator is not allowed.

    :param directory: The trusted base directory.
    :param untrusted: The untrusted path components relative to the
        base directory.
    :return: A safe path, otherwise ``None``.

    .. versionchanged:: 3.1.6
        Special device names in multi-segment paths are not allowed on Windows.

    .. versionchanged:: 3.1.5
        More special device names, regardless of extension or trailing spaces,
        are not allowed on Windows.

    .. versionchanged:: 3.1.4
        Special device names are not allowed on Windows.
    """
    if not directory:
        # Ensure we end up with ./path if directory="" is given,
        # otherwise the first untrusted part could become trusted.
        directory = "."

    parts = [directory]

    for part in untrusted:
        if not part:
            continue

        part = posixpath.normpath(part)

        if (
            os.path.isabs(part)
            # ntpath.isabs doesn't catch this
            or part.startswith("/")
            or part == ".."
            or part.startswith("../")
            or any(sep in part for sep in _os_alt_seps)
            or (
                os.name == "nt"
                and any(
                    p.partition(".")[0].strip().upper() in _windows_device_files
                    for p in part.split("/")
                )
            )
        ):
            return None

        parts.append(part)

    return posixpath.join(*parts)


def safe_join(base_dir: str, *parts: str) -> str:
    """
    Join path components and verify the result stays within base_dir.

    Resolves symlinks and '..' sequences, then checks the final path
    is a descendant of base_dir. Raises ValueError if traversal is
    detected.

    Args:
        base_dir: The trusted base directory.
        *parts: User-controlled path components to append.

    Returns:
        The resolved absolute path as a string.

    Raises:
        ValueError: If the resolved path escapes base_dir.
    """
    for part in parts:
        if "\x00" in part:
            raise ValueError("Path contains null byte")
    base = os.path.realpath(base_dir)
    resolved = os.path.realpath(os.path.join(base, *parts))
    if not (resolved.startswith(base + os.sep) or resolved == base):
        raise ValueError(f"Path {resolved!r} escapes base directory {base!r}")
    return resolved

