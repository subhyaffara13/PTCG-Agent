from pathlib import Path


def migrate_dir(src: str, dst: str) -> bool:
    """Migrate a directory from src to dst"""
    log = get_logger()
    src_path = Path(src)
    dst_path = Path(dst)
    if not any(src_path.iterdir()):
        log.debug("No files in %s", src)
        return False
    if dst_path.exists():
        if any(dst_path.iterdir()):
            # already exists, non-empty
            log.debug("%s already exists", dst)
            return False
        dst_path.rmdir()
    log.info("Copying %s -> %s", src, dst)
    ensure_dir_exists(dst_path.parent)
    shutil.copytree(src, dst, symlinks=True)
    return True

