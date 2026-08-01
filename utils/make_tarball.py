
def make_tarball(
    base_name: str,
    base_dir: str | os.PathLike[str],
    compress: Literal["gzip", "bzip2", "xz"] | None = "gzip",
    verbose: bool = False,
    owner: str | None = None,
    group: str | None = None,
) -> str:
    """Create a (possibly compressed) tar file from all the files under
    'base_dir'.

    'compress' must be "gzip" (the default), "bzip2", "xz", or None.

    'owner' and 'group' can be used to define an owner and a group for the
    archive that is being built. If not provided, the current owner and group
    will be used.

    The output tar file will be named 'base_dir' +  ".tar", possibly plus
    the appropriate compression extension (".gz", ".bz2", ".xz" or ".Z").

    Returns the output filename.
    """
    tar_compression = {
        'gzip': 'gz',
        'bzip2': 'bz2',
        'xz': 'xz',
        None: '',
    }
    compress_ext = {'gzip': '.gz', 'bzip2': '.bz2', 'xz': '.xz'}

    # flags for compression program, each element of list will be an argument
    if compress is not None and compress not in compress_ext.keys():
        raise ValueError(
            "bad value for 'compress': must be None, 'gzip', 'bzip2', 'xz'"
        )

    archive_name = base_name + '.tar'
    archive_name += compress_ext.get(compress, '')

    mkpath(os.path.dirname(archive_name))

    # creating the tarball
    import tarfile  # late import so Python build itself doesn't break

    log.info('Creating tar archive')

    uid = _get_uid(owner)
    gid = _get_gid(group)

    def _set_uid_gid(tarinfo):
        if gid is not None:
            tarinfo.gid = gid
            tarinfo.gname = group
        if uid is not None:
            tarinfo.uid = uid
            tarinfo.uname = owner
        return tarinfo

    tar = tarfile.open(archive_name, f'w|{tar_compression[compress]}')
    try:
        tar.add(base_dir, filter=_set_uid_gid)
    finally:
        tar.close()

    return archive_name

