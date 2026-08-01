
def _upload_xet_files(
    *,
    additions: list[CommitOperationAdd],
    repo_type: str,
    repo_id: str,
    headers: dict[str, str],
    endpoint: str | None = None,
    revision: str | None = None,
    create_pr: bool | None = None,
):
    """
    Uploads the content of `additions` to the Hub using the xet storage protocol.
    This chunks the files and deduplicates the chunks before uploading them to xetcas storage.

    Args:
        additions (`` of `CommitOperationAdd`):
            The files to be uploaded.
        repo_type (`str`):
            Type of the repo (e.g. `"model"`, `"dataset"`, `"space"`).
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated
            by a `/`.
        headers (`dict[str, str]`):
            Headers to use for the request, including authorization headers and user agent.
        endpoint: (`str`, *optional*):
            The endpoint to use for the xetcas service. Defaults to `constants.ENDPOINT`.
        revision (`str`, *optional*):
            The git revision to upload to.
        create_pr (`bool`, *optional*):
            Whether or not to create a Pull Request with that commit.

    Raises:
        [`EnvironmentError`](https://docs.python.org/3/library/exceptions.html#EnvironmentError)
            If an upload failed for any reason.
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If the server returns malformed responses or if the user is unauthorized to upload to xet storage.
        [`HfHubHTTPError`]
            If the LFS batch endpoint returned an HTTP error.

    **How it works:**
        The file upload system uses Xet storage, which is a content-addressable storage system that breaks files into chunks
        for efficient storage and transfer.

        ``session.new_upload_commit()`` manages uploading files by:
            - Registering upload tasks and starting upload immediately in the background
            - Breaking files into smaller chunks for efficient storage
            - Avoiding duplicate storage by recognizing identical chunks across files
            - Connecting to a storage server (CAS server) that manages these chunks

        Authentication works transparently: the upload commit accepts a ``token_refresh_url``
        that is used to refresh the short-lived xet write token as needed.

        The upload process works like this:
        1. Upload tasks run in parallel:
            1.1. Read the file content from a path, bytes array, or a stream.
            1.2. Split the file content into smaller chunks based on content patterns: each chunk gets a unique ID based on what's in it.
            1.3. For each chunk:
                - Check if it already exists in storage.
                - Skip uploading chunks that already exist.
            1.4. Group chunks into larger blocks for efficient transfer.
            1.5. Upload these blocks to the storage server.
            1.6. Assemble the file manifest locally and send it to the server for validation.
        2. Return reference files that contain information about the uploaded files, which can be used later to download them.
    """
    if len(additions) == 0:
        return

    # at this point, we know that hf_xet is installed
    from .utils._xet import (
        XetTokenType,
        abort_xet_session,
        get_xet_session,
        xet_connection_info_refresh_url,
        xet_headers_without_auth,
    )
    from .utils._xet_progress_reporting import XetProgressReporter

    refresh_url = xet_connection_info_refresh_url(
        token_type=XetTokenType.WRITE,
        repo_id=repo_id,
        repo_type=repo_type,
        revision=revision,
        endpoint=endpoint,
    )
    if create_pr:
        refresh_url += "?create_pr=1"

    xet_headers = xet_headers_without_auth(headers)

    import hf_xet

    session = get_xet_session()
    progress = None

    def _sha256_arg(op: CommitOperationAdd):
        # If the sha256 is already known, pass it to avoid recomputation. Otherwise let hf_xet
        # compute it while chunking the file (single read pass) and backfill it afterwards.
        return op.upload_info.sha256.hex() if op.upload_info.is_hashed else hf_xet.COMPUTE_SHA256

    try:
        if not are_progress_bars_disabled():
            progress = XetProgressReporter()
            progress_callback = progress.update_progress
        else:
            progress_callback = None

        all_bytes_ops = [op for op in additions if isinstance(op.path_or_fileobj, bytes)]
        all_paths_ops = [op for op in additions if isinstance(op.path_or_fileobj, (str, Path))]

        handles: list[tuple[CommitOperationAdd, Any]] = []
        with session.new_upload_commit(
            token_refresh_url=refresh_url,
            token_refresh_headers=headers,
            custom_headers=xet_headers,
            progress_callback=progress_callback,
        ) as commit:
            for op in all_paths_ops:
                handles.append((op, commit.start_upload_file(str(op.path_or_fileobj), sha256=_sha256_arg(op))))
            for op in all_bytes_ops:
                handles.append((op, commit.start_upload_bytes(op.path_or_fileobj, sha256=_sha256_arg(op))))

        # Backfill sha256 computed by hf_xet (needed later for the commit payload).
        for op, handle in handles:
            if not op.upload_info.is_hashed:
                op.upload_info.sha256 = bytes.fromhex(handle.result().xet_info.sha256)
    except KeyboardInterrupt:
        abort_xet_session()
        raise
    finally:
        if progress is not None:
            progress.close()

