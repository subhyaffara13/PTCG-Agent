import os

def make_archive(
    base_name: str,
    format: str,
    root_dir: str | os.PathLike[str] | bytes | os.PathLike[bytes] | None = None,
    base_dir: str | None = None,
    verbose: bool = False,
    owner: str | None = None,
    group: str | None = None,
) -> str: ...


def make_archive(
    base_name: str | os.PathLike[str],
    format: str,
    root_dir: str | os.PathLike[str] | bytes | os.PathLike[bytes],
    base_dir: str | None = None,
    verbose: bool = False,
    owner: str | None = None,
    group: str | None = None,
) -> str: ...


def make_archive(
    base_name: str | os.PathLike[str],
    format: str,
    root_dir: str | os.PathLike[str] | bytes | os.PathLike[bytes] | None = None,
    base_dir: str | None = None,
    verbose: bool = False,
    owner: str | None = None,
    group: str | None = None,
) -> str:
    """Create an archive file (eg. zip or tar).

    'base_name' is the name of the file to create, minus any format-specific
    extension; 'format' is the archive format: one of "zip", "tar", "gztar",
    "bztar", "xztar", or "ztar".

    'root_dir' is a directory that will be the root directory of the
    archive; ie. we typically chdir into 'root_dir' before creating the
    archive.  'base_dir' is the directory where we start archiving from;
    ie. 'base_dir' will be the common prefix of all files and
    directories in the archive.  'root_dir' and 'base_dir' both default
    to the current directory.  Returns the name of the archive file.

    'owner' and 'group' are used when creating a tar archive. By default,
    uses the current owner and group.
    """
    save_cwd = os.getcwd()
    if root_dir is not None:
        log.debug("changing into '%s'", root_dir)
        base_name = os.path.abspath(base_name)
        os.chdir(root_dir)

    if base_dir is None:
        base_dir = os.curdir

    kwargs: dict[str, bool | None] = {}

    try:
        format_info = ARCHIVE_FORMATS[format]
    except KeyError:
        raise ValueError(f"unknown archive format '{format}'")

    func = format_info[0]
    kwargs.update(format_info[1])

    if format != 'zip':
        kwargs['owner'] = owner
        kwargs['group'] = group

    try:
        filename = func(base_name, base_dir, **kwargs)
    finally:
        if root_dir is not None:
            log.debug("changing back to '%s'", save_cwd)
            os.chdir(save_cwd)

    return filename

