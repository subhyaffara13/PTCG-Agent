
def untar_file(filename: str, location: str) -> None:
    """
    Untar the file (with path `filename`) to the destination `location`.
    All files are written based on system defaults and umask (i.e. permissions
    are not preserved), except that regular file members with any execute
    permissions (user, group, or world) have "chmod +x" applied on top of the
    default.  Note that for windows, any execute changes using os.chmod are
    no-ops per the python docs.
    """
    ensure_dir(location)
    if filename.lower().endswith(".gz") or filename.lower().endswith(".tgz"):
        mode = "r:gz"
    elif filename.lower().endswith(BZ2_EXTENSIONS):
        mode = "r:bz2"
    elif filename.lower().endswith(XZ_EXTENSIONS):
        mode = "r:xz"
    elif filename.lower().endswith(".tar"):
        mode = "r"
    else:
        logger.warning(
            "Cannot determine compression type for file %s",
            filename,
        )
        mode = "r:*"

    tar = tarfile.open(filename, mode, encoding="utf-8")  # type: ignore
    try:
        leading = has_leading_dir([member.name for member in tar.getmembers()])

        # PEP 706 added `tarfile.data_filter`, and made some other changes to
        # Python's tarfile module (see below). The features were backported to
        # security releases.
        try:
            data_filter = tarfile.data_filter
        except AttributeError:
            _untar_without_filter(filename, location, tar, leading)
        else:
            default_mode_plus_executable = _get_default_mode_plus_executable()

            if leading:
                # Strip the leading directory from all files in the archive,
                # including hardlink targets (which are relative to the
                # unpack location).
                for member in tar.getmembers():
                    name_lead, name_rest = split_leading_dir(member.name)
                    member.name = name_rest
                    if member.islnk():
                        lnk_lead, lnk_rest = split_leading_dir(member.linkname)
                        if lnk_lead == name_lead:
                            member.linkname = lnk_rest

            def pip_filter(member: tarfile.TarInfo, path: str) -> tarfile.TarInfo:
                orig_mode = member.mode
                try:
                    try:
                        member = data_filter(member, location)
                    except tarfile.LinkOutsideDestinationError:
                        if sys.version_info[:3] in {
                            (3, 9, 17),
                            (3, 10, 12),
                            (3, 11, 4),
                        }:
                            # The tarfile filter in specific Python versions
                            # raises LinkOutsideDestinationError on valid input
                            # (https://github.com/python/cpython/issues/107845)
                            # Ignore the error there, but do use the
                            # more lax `tar_filter`
                            member = tarfile.tar_filter(member, location)
                        else:
                            raise
                except tarfile.TarError as exc:
                    message = "Invalid member in the tar file {}: {}"
                    # Filter error messages mention the member name.
                    # No need to add it here.
                    raise InstallationError(
                        message.format(
                            filename,
                            exc,
                        )
                    )
                if member.isfile() and orig_mode & 0o111:
                    member.mode = default_mode_plus_executable
                else:
                    # See PEP 706 note above.
                    # The PEP changed this from `int` to `Optional[int]`,
                    # where None means "use the default". Mypy doesn't
                    # know this yet.
                    member.mode = None  # type: ignore [assignment]
                return member

            tar.extractall(location, filter=pip_filter)

    finally:
        tar.close()

