
def find_prefixed(root: Path, prefix: str) -> Iterator[os.DirEntry[str]]:
    """Find all elements in root that begin with the prefix, case-insensitive."""
    l_prefix = prefix.lower()
    for x in os.scandir(root):
        if x.name.lower().startswith(l_prefix):
            yield x

