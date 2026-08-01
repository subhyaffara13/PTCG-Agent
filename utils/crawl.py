
def crawl(finder: SourceFinder, f: str) -> tuple[str, str]:
    module, base_dir = finder.crawl_up(f)
    return module, normalise_path(base_dir)

