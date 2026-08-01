
def walk_egg(egg_dir: StrPath) -> Iterator[tuple[str, list[str], list[str]]]:
    """Walk an unpacked egg's contents, skipping the metadata directory"""
    walker = sorted_walk(egg_dir)
    base, dirs, files = next(walker)
    if 'EGG-INFO' in dirs:
        dirs.remove('EGG-INFO')
    yield base, dirs, files
    yield from walker

