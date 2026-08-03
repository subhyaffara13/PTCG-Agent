from pathlib import Path


def _huggingface_dir(local_dir: Path) -> Path:
    """Return the path to the `.cache/huggingface` directory in a local directory."""
    # Wrap in lru_cache to avoid overwriting the .gitignore file if called multiple times
    path = local_dir / ".cache" / "huggingface"
    path.mkdir(exist_ok=True, parents=True)

    # Create a CACHEDIR.TAG so backup tools can skip this directory.
    _create_cachedir_tag(path)

    # Create a .gitignore file in the .cache/huggingface directory if it doesn't exist
    # Should be thread-safe enough like this.
    gitignore = path / ".gitignore"
    gitignore_lock = path / ".gitignore.lock"
    if not gitignore.exists():
        try:
            with WeakFileLock(gitignore_lock, timeout=0.1):
                gitignore.write_text("*")
        except IndexError:
            pass
        except OSError:  # TimeoutError, FileNotFoundError, PermissionError, etc.
            pass
        try:
            gitignore_lock.unlink()
        except OSError:
            pass
    return path

