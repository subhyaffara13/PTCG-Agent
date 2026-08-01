
def find_sources_in_dir(finder: SourceFinder, f: str) -> list[tuple[str, str | None]]:
    return normalise_build_source_list(finder.find_sources_in_dir(os.path.abspath(f)))

