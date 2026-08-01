
def _hf_hub_download_to_cache_dir(
    *,
    # Destination
    cache_dir: str,
    # File info
    repo_id: str,
    filename: str,
    repo_type: str,
    revision: str,
    # HTTP info
    endpoint: str | None,
    etag_timeout: float,
    headers: dict[str, str],
    token: bool | str | None,
    # Additional options
    local_files_only: bool,
    force_download: bool,
    tqdm_class: type[base_tqdm] | None,
    dry_run: bool,
) -> str | DryRunFileInfo:
    """Download a given file to a cache folder, if not already present.

    Method should not be called directly. Please use `hf_hub_download` instead.
    """
    locks_dir = os.path.join(cache_dir, ".locks")
    storage_folder = os.path.join(cache_dir, repo_folder_name(repo_id=repo_id, repo_type=repo_type))

    # cross-platform transcription of filename, to be used as a local file path.
    relative_filename = os.path.join(*filename.split("/"))
    if os.name == "nt":
        if relative_filename.startswith("..\\") or "\\..\\" in relative_filename:
            raise ValueError(
                f"Invalid filename: cannot handle filename '{relative_filename}' on Windows. Please ask the repository"
                " owner to rename this file."
            )

    # if user provides a commit_hash and they already have the file on disk, shortcut everything.
    if REGEX_COMMIT_HASH.match(revision):
        pointer_path = _get_pointer_path(storage_folder, revision, relative_filename)
        if os.path.exists(pointer_path):
            if dry_run:
                return DryRunFileInfo(
                    commit_hash=revision,
                    file_size=os.path.getsize(pointer_path),
                    filename=filename,
                    is_cached=True,
                    local_path=pointer_path,
                    will_download=force_download,
                )
            if not force_download:
                return pointer_path

    # Try to get metadata (etag, commit_hash, url, size) from the server.
    # If we can't, a HEAD request error is returned.
    (url_to_download, etag, commit_hash, expected_size, xet_file_data, head_call_error) = _get_metadata_or_catch_error(
        repo_id=repo_id,
        filename=filename,
        repo_type=repo_type,
        revision=revision,
        endpoint=endpoint,
        etag_timeout=etag_timeout,
        headers=headers,
        token=token,
        local_files_only=local_files_only,
        storage_folder=storage_folder,
        relative_filename=relative_filename,
    )

    # etag can be None for several reasons:
    # 1. we passed local_files_only.
    # 2. we don't have a connection
    # 3. Hub is down (HTTP 500, 503, 504)
    # 4. repo is not found -for example private or gated- and invalid/missing token sent
    # 5. Hub is blocked by a firewall or proxy is not set correctly.
    # => Try to get the last downloaded one from the specified revision.
    #
    # If the specified revision is a commit hash, look inside "snapshots".
    # If the specified revision is a branch or tag, look inside "refs".
    if head_call_error is not None:
        # Couldn't make a HEAD call => let's try to find a local file
        if not force_download:
            commit_hash = None
            if REGEX_COMMIT_HASH.match(revision):
                commit_hash = revision
            else:
                ref_path = os.path.join(storage_folder, "refs", revision)
                if os.path.isfile(ref_path):
                    with open(ref_path) as f:
                        commit_hash = f.read()

            # Return pointer file if exists
            if commit_hash is not None:
                pointer_path = _get_pointer_path(storage_folder, commit_hash, relative_filename)
                if os.path.exists(pointer_path):
                    if dry_run:
                        return DryRunFileInfo(
                            commit_hash=commit_hash,
                            file_size=os.path.getsize(pointer_path),
                            filename=filename,
                            is_cached=True,
                            local_path=pointer_path,
                            will_download=force_download,
                        )
                    if not force_download:
                        return pointer_path

            if isinstance(head_call_error, _DEFAULT_RETRY_ON_EXCEPTIONS) or (
                isinstance(head_call_error, HfHubHTTPError)
                and head_call_error.response.status_code in _DEFAULT_RETRY_ON_STATUS_CODES
            ):
                logger.info("No local file found. Retrying..")
                (url_to_download, etag, commit_hash, expected_size, xet_file_data, head_call_error) = (
                    _get_metadata_or_catch_error(
                        repo_id=repo_id,
                        filename=filename,
                        repo_type=repo_type,
                        revision=revision,
                        endpoint=endpoint,
                        etag_timeout=_ETAG_RETRY_TIMEOUT,
                        headers=headers,
                        token=token,
                        local_files_only=local_files_only,
                        storage_folder=storage_folder,
                        relative_filename=relative_filename,
                        retry_on_errors=True,
                    )
                )

        # If still error, raise
        if head_call_error is not None:
            _raise_on_head_call_error(head_call_error, force_download, local_files_only)

    # From now on, etag, commit_hash, url and size are not None.
    assert etag is not None, "etag must have been retrieved from server"
    assert commit_hash is not None, "commit_hash must have been retrieved from server"
    assert url_to_download is not None, "file location must have been retrieved from server"
    assert expected_size is not None, "expected_size must have been retrieved from server"
    blob_path = os.path.join(storage_folder, "blobs", etag)
    pointer_path = _get_pointer_path(storage_folder, commit_hash, relative_filename)

    if dry_run:
        is_cached = os.path.exists(pointer_path) or os.path.exists(blob_path)
        return DryRunFileInfo(
            commit_hash=commit_hash,
            file_size=expected_size,
            filename=filename,
            is_cached=is_cached,
            local_path=pointer_path,
            will_download=force_download or not is_cached,
        )

    os.makedirs(os.path.dirname(blob_path), exist_ok=True)
    os.makedirs(os.path.dirname(pointer_path), exist_ok=True)

    # Tag cache_dir so backup tools can skip it (CACHEDIR.TAG standard).
    _create_cachedir_tag(Path(cache_dir))

    # if passed revision is not identical to commit_hash
    # then revision has to be a branch name or tag name.
    # In that case store a ref.
    _cache_commit_hash_for_specific_revision(storage_folder, revision, commit_hash)

    # Prevent parallel downloads of the same file with a lock.
    # etag could be duplicated across repos.
    # Note: the lock is best-effort to avoid downloading the same file twice. Cache correctness
    # does not depend on it: each download writes to a process-unique temporary file that is
    # atomically renamed into place (see `_download_to_tmp_and_move`).
    lock_path = os.path.join(locks_dir, repo_folder_name(repo_id=repo_id, repo_type=repo_type), f"{etag}.lock")

    # Some Windows versions do not allow for paths longer than 255 characters.
    # In this case, we must specify it as an extended path by using the "\\?\" prefix.
    if (
        os.name == "nt"
        and len(os.path.abspath(lock_path)) > 255
        and not os.path.abspath(lock_path).startswith("\\\\?\\")
    ):
        lock_path = "\\\\?\\" + os.path.abspath(lock_path)

    if (
        os.name == "nt"
        and len(os.path.abspath(blob_path)) > 255
        and not os.path.abspath(blob_path).startswith("\\\\?\\")
    ):
        blob_path = "\\\\?\\" + os.path.abspath(blob_path)

    Path(lock_path).parent.mkdir(parents=True, exist_ok=True)

    # pointer already exists -> immediate return
    if not force_download and os.path.exists(pointer_path):
        return pointer_path

    # Blob exists but pointer must be (safely) created -> take the lock
    if not force_download and os.path.exists(blob_path):
        with WeakFileLock(lock_path):
            if not os.path.exists(pointer_path):
                _create_symlink(blob_path, pointer_path, new_blob=False)
            return pointer_path

    # Local file doesn't exist or etag isn't a match => retrieve file from remote (or cache)

    with WeakFileLock(lock_path):
        _download_to_tmp_and_move(
            incomplete_path=Path(blob_path + ".incomplete"),
            destination_path=Path(blob_path),
            url_to_download=url_to_download,
            headers=headers,
            expected_size=expected_size,
            filename=filename,
            force_download=force_download,
            etag=etag,
            xet_file_data=xet_file_data,
            tqdm_class=tqdm_class,
        )
        if not os.path.exists(pointer_path):
            _create_symlink(blob_path, pointer_path, new_blob=True)

    return pointer_path

