
def get_sources(
    fscache: FileSystemCache,
    modules: dict[str, str],
    changed_modules: list[tuple[str, str]],
    followed: bool,
) -> list[BuildSource]:
    sources = []
    for id, path in changed_modules:
        if fscache.isfile(path):
            sources.append(BuildSource(path, id, None, followed=followed))
    return sources

