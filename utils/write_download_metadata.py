
def write_download_metadata(local_dir: Path, filename: str, commit_hash: str, etag: str) -> None:
    """Write metadata about a file in the local directory related to a download process.

    Args:
        local_dir (`Path`):
            Path to the local directory in which files are downloaded.
    """
    paths = get_local_download_paths(local_dir, filename)
    with WeakFileLock(paths.lock_path):
        with paths.metadata_path.open("w") as f:
            f.write(f"{commit_hash}\n{etag}\n{time.time()}\n")

