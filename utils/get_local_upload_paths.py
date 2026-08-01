
def get_local_upload_paths(local_dir: Path, filename: str) -> LocalUploadFilePaths:
    """Compute paths to the files related to an upload process.

    Folders containing the paths are all guaranteed to exist.

    Args:
        local_dir (`Path`):
            Path to the local directory that is uploaded.
        filename (`str`):
            Path of the file in the repo.

    Return:
        [`LocalUploadFilePaths`]: the paths to the files (file_path, lock_path, metadata_path).
    """
    # filename is the path in the Hub repository (separated by '/')
    # make sure to have a cross-platform transcription
    sanitized_filename = os.path.join(*filename.split("/"))
    if os.name == "nt":
        if sanitized_filename.startswith("..\\") or "\\..\\" in sanitized_filename:
            raise ValueError(
                f"Invalid filename: cannot handle filename '{sanitized_filename}' on Windows. Please ask the repository"
                " owner to rename this file."
            )
    file_path = local_dir / sanitized_filename
    metadata_path = _huggingface_dir(local_dir) / "upload" / f"{sanitized_filename}.metadata"
    lock_path = metadata_path.with_suffix(".lock")

    # Some Windows versions do not allow for paths longer than 255 characters.
    # In this case, we must specify it as an extended path by using the "\\?\" prefix
    if os.name == "nt":
        if not str(local_dir).startswith("\\\\?\\") and len(os.path.abspath(lock_path)) > 255:
            file_path = Path("\\\\?\\" + os.path.abspath(file_path))
            lock_path = Path("\\\\?\\" + os.path.abspath(lock_path))
            metadata_path = Path("\\\\?\\" + os.path.abspath(metadata_path))

    file_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    return LocalUploadFilePaths(
        path_in_repo=filename, file_path=file_path, lock_path=lock_path, metadata_path=metadata_path
    )

