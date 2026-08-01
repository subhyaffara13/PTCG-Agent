
def get_header_deps(cfiles: list[tuple[str, str]]) -> list[tuple[bool, str]]:
    """Find all the headers directly included by a group of cfiles.

    Returns a sorted, deduplicated list of `(is_angled, header_name)` pairs.
    Callers that only need the names can ignore the bool, but it is needed by
    `resolve_cfile_deps` to apply the correct preprocessor search order.

    We do this by just regexping the source, which is a bit simpler than
    properly plumbing the data through. Transitive header-to-header includes
    are picked up by `resolve_cfile_deps` in `mypyc_build`, which can read
    the on-disk headers after every group has written its files.

    Arguments:
        cfiles: A list of (file name, file contents) pairs. Contents must be
            non-empty; callers handling cached groups must re-read the .c
            from disk before calling, otherwise direct includes are missed
            and Extension.depends ends up empty.
    """
    assert all(
        contents for _, contents in cfiles
    ), "get_header_deps requires non-empty file contents"
    headers: set[tuple[bool, str]] = set()
    for _, contents in cfiles:
        headers.update(_extract_includes(contents))

    return sorted(headers)

