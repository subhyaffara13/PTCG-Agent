
def migrate_file(src: str | Path, dst: str | Path, substitutions: Any = None) -> bool:
    """Migrate a single file from src to dst

    substitutions is an optional dict of {regex: replacement} for performing replacements on the file.
    """
    log = get_logger()
    dst_path = Path(dst)
    if dst_path.exists():
        # already exists
        log.debug("%s already exists", dst)
        return False
    log.info("Copying %s -> %s", src, dst)
    ensure_dir_exists(dst_path.parent)
    shutil.copy(src, dst)
    if substitutions:
        with dst_path.open() as f:
            text = f.read()
        for pat, replacement in substitutions.items():
            text = pat.sub(replacement, text)
        with dst_path.open("w") as f:
            f.write(text)
    return True

