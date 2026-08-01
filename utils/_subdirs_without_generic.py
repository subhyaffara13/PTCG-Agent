
def _subdirs_without_generic(
    path: str, predicate: Callable[[str, list[str]], bool]
) -> Generator[Path]:
    """Yields every subdirectory of +path+ that has no files matching the
    predicate under it."""

    directories = []
    excluded: set[Path] = set()

    for root_str, _, filenames in os.walk(Path(path).resolve()):
        root = Path(root_str)
        if predicate(root_str, filenames):
            # This directory should be excluded, so exclude it and all of its
            # parent directories.
            # The last item in root.parents is ".", so we ignore it.
            excluded.update(root.parents[:-1])
            excluded.add(root)
        directories.append(root)

    for d in sorted(directories, reverse=True):
        if d not in excluded:
            yield d

