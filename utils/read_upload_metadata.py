import time
from pathlib import Path


def read_upload_metadata(local_dir: Path, filename: str) -> LocalUploadFileMetadata:
    """Read metadata about a file in the local directory related to an upload process.

    TODO: factorize logic with `read_download_metadata`.

    Args:
        local_dir (`Path`):
            Path to the local directory in which files are downloaded.
        filename (`str`):
            Path of the file in the repo.

    Return:
        `[LocalUploadFileMetadata]` or `None`: the metadata if it exists, `None` otherwise.
    """
    paths = get_local_upload_paths(local_dir, filename)
    with WeakFileLock(paths.lock_path):
        if paths.metadata_path.exists():
            try:
                with paths.metadata_path.open() as f:
                    timestamp = float(f.readline().strip())

                    size = int(f.readline().strip())  # never None

                    _should_ignore = f.readline().strip()
                    should_ignore = None if _should_ignore == "" else bool(int(_should_ignore))

                    _sha256 = f.readline().strip()
                    sha256 = None if _sha256 == "" else _sha256

                    _upload_mode = f.readline().strip()
                    upload_mode = None if _upload_mode == "" else _upload_mode
                    if upload_mode not in (None, "regular", "lfs"):
                        raise ValueError(f"Invalid upload mode in metadata {paths.path_in_repo}: {upload_mode}")

                    _remote_oid = f.readline().strip()
                    remote_oid = None if _remote_oid == "" else _remote_oid

                    is_uploaded = bool(int(f.readline().strip()))
                    is_committed = bool(int(f.readline().strip()))

                    metadata = LocalUploadFileMetadata(
                        timestamp=timestamp,
                        size=size,
                        should_ignore=should_ignore,
                        sha256=sha256,
                        upload_mode=upload_mode,
                        remote_oid=remote_oid,
                        is_uploaded=is_uploaded,
                        is_committed=is_committed,
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

                # corrupted metadata => we don't know anything expect its size
                return LocalUploadFileMetadata(size=paths.file_path.stat().st_size)

            # TODO: can we do better?
            if (
                metadata.timestamp is not None
                and metadata.is_uploaded  # file was uploaded
                and not metadata.is_committed  # but not committed
                and time.time() - metadata.timestamp > 20 * 3600  # and it's been more than 20 hours
            ):  # => we consider it as garbage-collected by S3
                metadata.is_uploaded = False

            # check if the file exists and hasn't been modified since the metadata was saved
            try:
                if metadata.timestamp is not None and paths.file_path.stat().st_mtime <= metadata.timestamp:
                    return metadata
                logger.info(f"Ignored metadata for '{filename}' (outdated). Will re-compute hash.")
            except FileNotFoundError:
                # file does not exist => metadata is outdated
                pass

    # empty metadata => we don't know anything expect its size
    return LocalUploadFileMetadata(size=paths.file_path.stat().st_size)

