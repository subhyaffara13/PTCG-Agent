import os

def find_sources(
    paths: list[str], options: Options, fscache: FileSystemCache
) -> list[tuple[str, str | None]]:
    paths = [os.path.abspath(p) for p in paths]
    return normalise_build_source_list(create_source_list(paths, options, fscache))

