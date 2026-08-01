
def Cache_makedir(self: Cache, name: str) -> LEGACY_PATH:
    """Return a directory path object with the given name.

    Same as :func:`mkdir`, but returns a legacy py path instance.
    """
    return legacy_path(self.mkdir(name))

