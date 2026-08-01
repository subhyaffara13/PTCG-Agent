
def _force_symlink(root: Path, target: str | PurePath, link_to: str | Path) -> None:
    """Helper to create the current symlink.

    It's full of race conditions that are reasonably OK to ignore
    for the context of best effort linking to the latest test run.

    The presumption being that in case of much parallelism
    the inaccuracy is going to be acceptable.
    """
    current_symlink = root.joinpath(target)
    try:
        current_symlink.unlink()
    except OSError:
        pass
    try:
        current_symlink.symlink_to(link_to)
    except Exception:
        pass

