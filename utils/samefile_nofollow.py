
def samefile_nofollow(p1: Path, p2: Path) -> bool:
    """Test whether two paths reference the same actual file or directory.

    Unlike Path.samefile(), does not resolve symlinks.
    """
    return os.path.samestat(p1.lstat(), p2.lstat())

