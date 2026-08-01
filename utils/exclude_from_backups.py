
def exclude_from_backups(target_dir: str) -> None:
    """Exclude the directory from various archives and backups supporting CACHEDIR.TAG.

    If the CACHEDIR.TAG file exists the function is a no-op.
    """
    cachedir_tag = os_path_join(target_dir, "CACHEDIR.TAG")
    try:
        with open(cachedir_tag, "x") as f:
            f.write("""Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag automatically created by mypy.
# For information about cache directory tags see https://bford.info/cachedir/
""")
    except FileExistsError:
        pass

