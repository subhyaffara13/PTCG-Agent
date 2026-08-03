from pathlib import Path


def make_numbered_dir(root: Path, prefix: str, mode: int = 0o700) -> Path:
    """Create a directory with an increased number as suffix for the given prefix."""
    for i in range(10):
        # try up to 10 times to create the directory
        max_existing = max(map(parse_num, find_suffixes(root, prefix)), default=-1)
        new_number = max_existing + 1
        new_path = root.joinpath(f"{prefix}{new_number}")
        try:
            new_path.mkdir(mode=mode)
        except Exception:
            pass
        else:
            _force_symlink(root, prefix + "current", new_path)
            return new_path
    else:
        raise OSError(
            "could not create numbered dir with prefix "
            f"{prefix} in {root} after 10 tries"
        )

