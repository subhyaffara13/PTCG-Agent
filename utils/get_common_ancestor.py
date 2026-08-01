
def get_common_ancestor(
    invocation_dir: Path,
    paths: Iterable[Path],
) -> Path:
    common_ancestor: Path | None = None
    for path in paths:
        if not path.exists():
            continue
        if common_ancestor is None:
            common_ancestor = path
        else:
            if common_ancestor in path.parents or path == common_ancestor:
                continue
            elif path in common_ancestor.parents:
                common_ancestor = path
            else:
                shared = commonpath(path, common_ancestor)
                if shared is not None:
                    common_ancestor = shared
    if common_ancestor is None:
        common_ancestor = invocation_dir
    elif common_ancestor.is_file():
        common_ancestor = common_ancestor.parent
    return common_ancestor

