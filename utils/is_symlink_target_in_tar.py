import os

def is_symlink_target_in_tar(tar: tarfile.TarFile, tarinfo: tarfile.TarInfo) -> bool:
    """Check if the file pointed to by the symbolic link is in the tar archive"""
    linkname = os.path.join(os.path.dirname(tarinfo.name), tarinfo.linkname)

    linkname = os.path.normpath(linkname)
    linkname = linkname.replace("\\", "/")

    try:
        tar.getmember(linkname)
        return True
    except KeyError:
        return False

