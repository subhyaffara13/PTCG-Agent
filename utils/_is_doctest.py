
def _is_doctest(config: Config, path: Path, parent: Collector) -> bool:
    if path.suffix in (".txt", ".rst") and parent.session.isinitpath(path):
        return True
    globs = config.getoption("doctestglob") or ["test*.txt"]
    return any(fnmatch_ex(glob, path) for glob in globs)

