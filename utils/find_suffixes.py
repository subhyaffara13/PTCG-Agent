
def find_suffixes(root: Path, prefix: str) -> Iterator[str]:
    """Combine find_prefixes and extract_suffixes."""
    return extract_suffixes(find_prefixed(root, prefix), prefix)

