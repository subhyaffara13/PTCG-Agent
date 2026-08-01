
def create_source_list(
    paths: Sequence[str],
    options: Options,
    fscache: FileSystemCache | None = None,
    allow_empty_dir: bool = False,
) -> list[BuildSource]:
    """From a list of source files/directories, makes a list of BuildSources.

    Raises InvalidSourceList on errors.
    """
    fscache = fscache or FileSystemCache()
    finder = SourceFinder(fscache, options)

    sources = []
    for path in paths:
        path = os.path.normpath(path)
        if path.endswith(PY_EXTENSIONS):
            # Can raise InvalidSourceList if a directory doesn't have a valid module name.
            name, base_dir = finder.crawl_up(path)
            sources.append(BuildSource(path, name, None, base_dir))
        elif fscache.isdir(path):
            sub_sources = finder.find_sources_in_dir(path)
            if not sub_sources and not allow_empty_dir:
                raise InvalidSourceList(f"There are no .py[i] files in directory '{path}'")
            sources.extend(sub_sources)
        else:
            mod = os.path.basename(path) if options.scripts_are_modules else None
            sources.append(BuildSource(path, mod, None))
    return sources

