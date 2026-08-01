
def get_lib_dirs() -> Sequence[str]:
    """Gets the lib directory for linking to shared libraries.

    On some platforms, the package may need to be built specially to export
    development libraries.
    """
    return [_this_dir]

