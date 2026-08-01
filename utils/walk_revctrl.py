
def walk_revctrl(dirname='') -> Iterator:
    """Find all files under revision control"""
    for ep in metadata.entry_points(group='setuptools.file_finders'):
        yield from ep.load()(dirname)

