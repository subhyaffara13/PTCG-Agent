
def copy_directory_permissions(directory: str, target_file: BinaryIO) -> None:
    mode = (
        os.stat(directory).st_mode & 0o666  # select read/write permissions of directory
        | 0o600  # set owner read/write permissions
    )
    # Change permissions only if there is no risk of following a symlink.
    if os.chmod in os.supports_fd:
        os.chmod(target_file.fileno(), mode)
    elif os.chmod in os.supports_follow_symlinks:
        os.chmod(target_file.name, mode, follow_symlinks=False)

