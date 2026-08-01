
def _glob_paths_csv_transformer(value: str) -> Sequence[str]:
    """Transforms a comma separated list of paths while expanding user and
    variables and glob patterns.
    """
    paths: list[str] = []
    for path in _csv_transformer(value):
        paths.extend(glob(_path_transformer(path), recursive=True))
    return paths

