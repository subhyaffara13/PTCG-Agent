
def _find_common_roots(paths: t.Iterable[str]) -> t.Iterable[str]:
    root: dict[str, dict[str, t.Any]] = {}

    for chunks in sorted((PurePath(x).parts for x in paths), key=len, reverse=True):
        node = root

        for chunk in chunks:
            node = node.setdefault(chunk, {})

        node.clear()

    rv = set()

    def _walk(node: t.Mapping[str, dict[str, t.Any]], path: tuple[str, ...]) -> None:
        for prefix, child in node.items():
            _walk(child, path + (prefix,))

        # If there are no more nodes, and a path has been accumulated, add it.
        # Path may be empty if the "" entry is in sys.path.
        if not node and path:
            rv.add(os.path.join(*path))

    _walk(root, ())
    return rv

