
def move_file(src, dst, verbose=True):  # noqa: C901
    """Move a file 'src' to 'dst'.  If 'dst' is a directory, the file will
    be moved into it with the same name; otherwise, 'src' is just renamed
    to 'dst'.  Return the new full name of the file.

    Handles cross-device moves on Unix using 'copy_file()'.  What about
    other systems???
    """
    import errno
    from os.path import basename, dirname, exists, isdir, isfile

    if verbose >= 1:
        log.info("moving %s -> %s", src, dst)

    if not isfile(src):
        raise DistutilsFileError(f"can't move '{src}': not a regular file")

    if isdir(dst):
        dst = os.path.join(dst, basename(src))
    elif exists(dst):
        raise DistutilsFileError(
            f"can't move '{src}': destination '{dst}' already exists"
        )

    if not isdir(dirname(dst)):
        raise DistutilsFileError(
            f"can't move '{src}': destination '{dst}' not a valid path"
        )

    copy_it = False
    try:
        os.rename(src, dst)
    except OSError as e:
        (num, msg) = e.args
        if num == errno.EXDEV:
            copy_it = True
        else:
            raise DistutilsFileError(f"couldn't move '{src}' to '{dst}': {msg}")

    if copy_it:
        copy_file(src, dst, verbose=verbose)
        try:
            os.unlink(src)
        except OSError as e:
            (num, msg) = e.args
            try:
                os.unlink(dst)
            except OSError:
                pass
            raise DistutilsFileError(
                f"couldn't move '{src}' to '{dst}' by copy/delete: "
                f"delete '{src}' failed: {msg}"
            )
    return dst

