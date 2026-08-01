
def _is_archive_file(name):
    ext = _splitext(name)[1].lower()
    if ext in (
        # ZIP extensions
        ".zip",
        WHEEL_EXTENSION,
        # BZ2 extensions
        ".tar.bz2",
        ".tbz",
        # TAR extensions
        ".tar.gz",
        ".tgz",
        ".tar",
        # XZ extensions
        ".tar.xz",
        ".txz",
        ".tlz",
        ".tar.lz",
        ".tar.lzma",
    ):
        return True
    return False

