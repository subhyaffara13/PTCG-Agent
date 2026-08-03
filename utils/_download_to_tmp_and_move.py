import uuid
from pathlib import Path


def _download_to_tmp_and_move(
    incomplete_path: Path,
    destination_path: Path,
    url_to_download: str,
    headers: dict[str, str],
    expected_size: int | None,
    filename: str,
    force_download: bool,
    etag: str | None,
    xet_file_data: XetFileData | None,
    tqdm_class: type[base_tqdm] | None = None,
) -> None:
    """Download content from a URL to a destination path.

    Internal logic:
    - return early if file is already downloaded
    - check disk space before downloading
    - download content to a process-unique temporary file
    - set correct permissions on temporary file
    - move the temporary file to the destination path

    Both `incomplete_path` and `destination_path` must be on the same volume to avoid a local copy.
    """
    if destination_path.exists() and not force_download:
        # Do nothing if already exists (except if force_download=True)
        return

    # Download to a process-unique temporary file before moving it in place. A shared
    # `<etag>.incomplete` file corrupts the cache whenever the surrounding lock is not honored:
    # on some filesystems (Lustre, GPFS, some NFS mounts) `flock(2)` silently succeeds for every
    # caller and concurrent processes end up appending to the same file. With a unique file per
    # process, a broken lock costs only duplicated bandwidth: each process downloads the full
    # file and atomically renames it to the final destination.
    # See https://github.com/huggingface/huggingface_hub/pull/4228.
    tmp_path = incomplete_path.with_name(f"{incomplete_path.stem}.{uuid.uuid4().hex[:8]}.incomplete")
    try:
        with tmp_path.open("wb") as f:
            logger.debug(f"Downloading '{filename}' to '{tmp_path}'")

            if expected_size is not None:  # might be None if HTTP header not set correctly
                # Check disk space in both tmp and destination path
                _check_disk_space(expected_size, tmp_path.parent)
                _check_disk_space(expected_size, destination_path.parent)

            if xet_file_data is not None and is_xet_available():
                logger.debug("Xet Storage is enabled for this repo. Downloading file from Xet Storage..")
                xet_get(
                    incomplete_path=tmp_path,
                    xet_file_data=xet_file_data,
                    headers=headers,
                    expected_size=expected_size,
                    displayed_filename=filename,
                    tqdm_class=tqdm_class,
                )
            else:
                if xet_file_data is not None and not constants.HF_HUB_DISABLE_XET:
                    logger.warning(
                        "Xet Storage is enabled for this repo, but the 'hf_xet' package is not installed. "
                        "Falling back to regular HTTP download. "
                        "For better performance, install the package with: `pip install huggingface_hub[hf_xet]` or `pip install hf_xet`"
                    )

                http_get(
                    url_to_download,
                    f,
                    headers=headers,
                    expected_size=expected_size,
                    tqdm_class=tqdm_class,
                )

        logger.debug(f"Download complete. Moving file to {destination_path}")
        _chmod_and_move(tmp_path, destination_path)
    finally:
        # No-op on success (file has been moved). On failure, do not keep a partial file around:
        # it could not be reused anyway since the temporary name is unique to this download.
        tmp_path.unlink(missing_ok=True)

