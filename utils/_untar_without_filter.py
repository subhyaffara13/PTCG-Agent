import os

def _untar_without_filter(
    filename: str,
    location: str,
    tar: tarfile.TarFile,
    leading: bool,
) -> None:
    """Fallback for Python without tarfile.data_filter"""
    # NOTE: This function can be removed once pip requires CPython ≥ 3.12.​
    # PEP 706 added tarfile.data_filter, made tarfile extraction operations more secure.
    # This feature is fully supported from CPython 3.12 onward.
    for member in tar.getmembers():
        fn = member.name
        if leading:
            fn = split_leading_dir(fn)[1]
        path = os.path.join(location, fn)
        if not is_within_directory(location, path):
            message = (
                "The tar file ({}) has a file ({}) trying to install "
                "outside target directory ({})"
            )
            raise InstallationError(message.format(filename, path, location))
        if member.isdir():
            ensure_dir(path)
        elif member.issym():
            if not is_symlink_target_in_tar(tar, member):
                message = (
                    "The tar file ({}) has a file ({}) trying to install "
                    "outside target directory ({})"
                )
                raise InstallationError(
                    message.format(filename, member.name, member.linkname)
                )
            try:
                tar._extract_member(member, path)
            except Exception as exc:
                # Some corrupt tar files seem to produce this
                # (specifically bad symlinks)
                logger.warning(
                    "In the tar file %s the member %s is invalid: %s",
                    filename,
                    member.name,
                    exc,
                )
                continue
        else:
            try:
                fp = tar.extractfile(member)
            except (KeyError, AttributeError) as exc:
                # Some corrupt tar files seem to produce this
                # (specifically bad symlinks)
                logger.warning(
                    "In the tar file %s the member %s is invalid: %s",
                    filename,
                    member.name,
                    exc,
                )
                continue
            ensure_dir(os.path.dirname(path))
            assert fp is not None
            with open(path, "wb") as destfp:
                shutil.copyfileobj(fp, destfp)
            fp.close()
            # Update the timestamp (useful for cython compiled files)
            tar.utime(member, path)
            # member have any execute permissions for user/group/world?
            if member.mode & 0o111:
                set_extracted_file_to_default_mode_plus_executable(path)

