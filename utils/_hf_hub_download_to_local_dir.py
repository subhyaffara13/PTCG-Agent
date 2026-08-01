
def _hf_hub_download_to_local_dir(
    *,
    # Destination
    local_dir: str | Path,
    # File info
    repo_id: str,
    repo_type: str,
    filename: str,
    revision: str,
    # HTTP info
    endpoint: str | None,
    etag_timeout: float,
    headers: dict[str, str],
    token: bool | str | None,
    # Additional options
    cache_dir: str,
    force_download: bool,
    local_files_only: bool,
    tqdm_class: type[base_tqdm] | None,
    dry_run: bool,
) -> str | DryRunFileInfo:
    """Download a given file to a local folder, if not already present.

    Method should not be called directly. Please use `hf_hub_download` instead.
    """
    # Some Windows versions do not allow for paths longer than 255 characters.
    # In this case, we must specify it as an extended path by using the "\\?\" prefix.
    if os.name == "nt" and len(os.path.abspath(local_dir)) > 255:
        local_dir = "\\\\?\\" + os.path.abspath(local_dir)
    local_dir = Path(local_dir)
    paths = get_local_download_paths(local_dir=local_dir, filename=filename)
    local_metadata = read_download_metadata(local_dir=local_dir, filename=filename)

    # Local file exists + metadata exists + commit_hash matches => return file
    if (
        REGEX_COMMIT_HASH.match(revision)
        and paths.file_path.is_file()
        and local_metadata is not None
        and local_metadata.commit_hash == revision
    ):
        local_file = str(paths.file_path)
        if dry_run:
            return DryRunFileInfo(
                commit_hash=revision,
                file_size=os.path.getsize(local_file),
                filename=filename,
                is_cached=True,
                local_path=local_file,
                will_download=force_download,
            )
        if not force_download:
            return local_file

    # Local file doesn't exist or commit_hash doesn't match => we need the etag
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
    )

    if head_call_error is not None:
        # No HEAD call but local file exists => default to local file
        if paths.file_path.is_file():
            if dry_run or not force_download:
                logger.warning(
                    f"Couldn't access the Hub to check for update but local file already exists. Defaulting to existing file. (error: {head_call_error})"
                )
            local_path = str(paths.file_path)
            if dry_run and local_metadata is not None:
                return DryRunFileInfo(
                    commit_hash=local_metadata.commit_hash,
                    file_size=os.path.getsize(local_path),
                    filename=filename,
                    is_cached=True,
                    local_path=local_path,
                    will_download=force_download,
                )
            if not force_download:
                return local_path
        elif not force_download:
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

    # Local file exists => check if it's up-to-date
    if not force_download and paths.file_path.is_file():
        # etag matches => update metadata and return file
        if local_metadata is not None and local_metadata.etag == etag:
            write_download_metadata(local_dir=local_dir, filename=filename, commit_hash=commit_hash, etag=etag)
            if dry_run:
                return DryRunFileInfo(
                    commit_hash=commit_hash,
                    file_size=expected_size,
                    filename=filename,
                    is_cached=True,
                    local_path=str(paths.file_path),
                    will_download=False,
                )
            return str(paths.file_path)

        # metadata is outdated + etag is a sha256
        # => means it's an LFS file (large)
        # => let's compute local hash and compare
        # => if match, update metadata and return file
        if local_metadata is None and REGEX_SHA256.match(etag) is not None:
            with open(paths.file_path, "rb") as f:
                file_hash = sha_fileobj(f).hex()
            if file_hash == etag:
                write_download_metadata(local_dir=local_dir, filename=filename, commit_hash=commit_hash, etag=etag)
                if dry_run:
                    return DryRunFileInfo(
                        commit_hash=commit_hash,
                        file_size=expected_size,
                        filename=filename,
                        is_cached=True,
                        local_path=str(paths.file_path),
                        will_download=False,
                    )
                return str(paths.file_path)

    # Local file doesn't exist or etag isn't a match => retrieve file from remote (or cache)

    # If we are lucky enough, the file is already in the cache => copy it
    if not force_download:
        cached_path = try_to_load_from_cache(
            repo_id=repo_id,
            filename=filename,
            cache_dir=cache_dir,
            revision=commit_hash,
            repo_type=repo_type,
        )
        if isinstance(cached_path, str):
            with WeakFileLock(paths.lock_path):
                paths.file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(cached_path, paths.file_path)
            write_download_metadata(local_dir=local_dir, filename=filename, commit_hash=commit_hash, etag=etag)
            if dry_run:
                return DryRunFileInfo(
                    commit_hash=commit_hash,
                    file_size=expected_size,
                    filename=filename,
                    is_cached=True,
                    local_path=str(paths.file_path),
                    will_download=False,
                )
            return str(paths.file_path)

    if dry_run:
        is_cached = paths.file_path.is_file()
        return DryRunFileInfo(
            commit_hash=commit_hash,
            file_size=expected_size,
            filename=filename,
            is_cached=is_cached,
            local_path=str(paths.file_path),
            will_download=force_download or not is_cached,
        )

    # Otherwise, let's download the file!
    with WeakFileLock(paths.lock_path):
        paths.file_path.unlink(missing_ok=True)  # delete outdated file first
        _download_to_tmp_and_move(
            incomplete_path=paths.incomplete_path(etag),
            destination_path=paths.file_path,
            url_to_download=url_to_download,
            headers=headers,
            expected_size=expected_size,
            filename=filename,
            force_download=force_download,
            etag=etag,
            xet_file_data=xet_file_data,
            tqdm_class=tqdm_class,
        )

    write_download_metadata(local_dir=local_dir, filename=filename, commit_hash=commit_hash, etag=etag)
    return str(paths.file_path)

