from pathlib import Path


def migrate_one(src: str, dst: str) -> bool:
    """Migrate one item

    dispatches to migrate_dir/_file
    """
    log = get_logger()
    if Path(src).is_file():
        return migrate_file(src, dst)
    if Path(src).is_dir():
        return migrate_dir(src, dst)
    log.debug("Nothing to migrate for %s", src)
    return False

