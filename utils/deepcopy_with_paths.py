
def deepcopy_with_paths(item: _T, paths: Sequence[Sequence[str]]) -> _T:
    """Copy only the containers along the given paths.

    Used to guard against mutation by extract_files without copying the entire structure.
    Only dicts and lists that lie on a path are copied; everything else
    is returned by reference.

    For example, given paths=[["foo", "files", "file"]] and the structure:
        {
            "foo": {
                "bar": {"baz": {}},
                "files": {"file": <content>}
            }
        }
    The root dict, "foo", and "files" are copied (they lie on the path).
    "bar" and "baz" are returned by reference (off the path).
    """
    return _deepcopy_with_paths(item, paths, 0)

