from pathlib import Path


def cleanup_dead_symlinks(root: Path) -> None:
    for left_dir in root.iterdir():
        if left_dir.is_symlink():
            if not left_dir.resolve().exists():
                left_dir.unlink()

