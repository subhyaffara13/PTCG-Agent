import pathlib

def mkpath(name: pathlib.Path, mode=0o777, verbose=True) -> None:
    """Create a directory and any missing ancestor directories.

    If the directory already exists (or if 'name' is the empty string, which
    means the current directory, which of course exists), then do nothing.
    Raise DistutilsFileError if unable to create some directory along the way
    (eg. some sub-path exists, but is a file rather than a directory).
    If 'verbose' is true, log the directory created.
    """
    if verbose and not name.is_dir():
        log.info("creating %s", name)

    try:
        name.mkdir(mode=mode, parents=True, exist_ok=True)
    except OSError as exc:
        raise DistutilsFileError(f"could not create '{name}': {exc.args[-1]}")

