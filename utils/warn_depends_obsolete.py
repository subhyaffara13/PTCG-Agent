
def warn_depends_obsolete(cmd, basename, filename) -> None:
    """
    Unused: left to avoid errors when updating (from source) from <= 67.8.
    Old installations have a .dist-info directory with the entry-point
    ``depends.txt = setuptools.command.egg_info:warn_depends_obsolete``.
    This may trigger errors when running the first egg_info in build_meta.
    TODO: Remove this function in a version sufficiently > 68.
    """

