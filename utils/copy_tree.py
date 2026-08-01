
def copy_tree(
    src,
    dst,
    preserve_mode=True,
    preserve_times=True,
    preserve_symlinks=False,
    update=False,
    verbose=True,
):
    """Copy an entire directory tree 'src' to a new location 'dst'.

    Both 'src' and 'dst' must be directory names.  If 'src' is not a
    directory, raise DistutilsFileError.  If 'dst' does not exist, it is
    created with 'mkpath()'.  The end result of the copy is that every
    file in 'src' is copied to 'dst', and directories under 'src' are
    recursively copied to 'dst'.  Return the list of files that were
    copied or might have been copied, using their output name.  The
    return value is unaffected by 'update': it is simply
    the list of all files under 'src', with the names changed to be
    under 'dst'.

    'preserve_mode' and 'preserve_times' are the same as for
    'copy_file'; note that they only apply to regular files, not to
    directories.  If 'preserve_symlinks' is true, symlinks will be
    copied as symlinks (on platforms that support them!); otherwise
    (the default), the destination of the symlink will be copied.
    'update' and 'verbose' are the same as for 'copy_file'.
    """
    if not os.path.isdir(src):
        raise DistutilsFileError(f"cannot copy tree '{src}': not a directory")
    try:
        names = os.listdir(src)
    except OSError as e:
        raise DistutilsFileError(f"error listing files in '{src}': {e.strerror}")

    mkpath(dst, verbose=verbose)

    copy_one = functools.partial(
        _copy_one,
        src=src,
        dst=dst,
        preserve_symlinks=preserve_symlinks,
        verbose=verbose,
        preserve_mode=preserve_mode,
        preserve_times=preserve_times,
        update=update,
    )
    return list(itertools.chain.from_iterable(map(copy_one, names)))

