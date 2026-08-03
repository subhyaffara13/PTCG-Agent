from pathlib import Path


def read_download_metadata(local_dir: Path, filename: str) -> LocalDownloadFileMetadata | None:
    """Read metadata about a file in the local directory related to a download process.

    Args:
        local_dir (`Path`):
            Path to the local directory in which files are downloaded.
        filename (`str`):
            Path of the file in the repo.

    Return:
        `[LocalDownloadFileMetadata]` or `None`: the metadata if it exists, `None` otherwise.
    """
    paths = get_local_download_paths(local_dir, filename)
    with WeakFileLock(paths.lock_path):
        if paths.metadata_path.exists():
            try:
                with paths.metadata_path.open() as f:
                    commit_hash = f.readline().strip()
                    etag = f.readline().strip()
                    timestamp = float(f.readline().strip())
                    metadata = LocalDownloadFileMetadata(
                        filename=filename,
                        commit_hash=commit_hash,
                        etag=etag,
                        timestamp=timestamp,
                    )
            except Exception as e:
                # remove the metadata file if it is corrupted / not the right format
                logger.warning(
                    f"Invalid metadata file {paths.metadata_path}: {e}. Removing it from disk and continue."
                )
                try:
                    paths.metadata_path.unlink()
                except Exception as e:
                    logger.warning(f"Could not remove corrupted metadata file {paths.metadata_path}: {e}")
                return None

            try:
                # check if the file exists and hasn't been modified since the metadata was saved
                stat = paths.file_path.stat()
                if (
                    stat.st_mtime - 1 <= metadata.timestamp
                ):  # allow 1s difference as stat.st_mtime might not be precise
                    return metadata
                logger.info(f"Ignored metadata for '{filename}' (outdated). Will re-compute hash.")
            except FileNotFoundError:
                # file does not exist => metadata is outdated
                return None
    return None

