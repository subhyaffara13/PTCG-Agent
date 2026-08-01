
def _copy_no_matter_what(src: str, dst: str) -> None:
    """Copy file from src to dst.

    If `shutil.copy2` fails, fallback to `shutil.copyfile`.
    """
    try:
        # Copy file with metadata and permission
        # Can fail e.g. if dst is an S3 mount
        shutil.copy2(src, dst)
    except OSError:
        # Copy only file content
        shutil.copyfile(src, dst)

