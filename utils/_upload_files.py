
def _upload_files(
    *,
    additions: list[CommitOperationAdd],
    repo_type: str,
    repo_id: str,
    headers: dict[str, str],
    endpoint: str | None = None,
    num_threads: int = 5,
    revision: str | None = None,
    create_pr: bool | None = None,
):
    """
    Uploads the files through the Xet protocol if possible, otherwise through the legacy LFS protocol.

    The Xet path does not require any Python-side sha256 computation: hashing happens inside `hf_xet`
    while chunking the files (single read pass) and is backfilled on the operations afterwards.
    """
    has_buffered_io_data = any(isinstance(op.path_or_fileobj, io.BufferedIOBase) for op in additions)
    if is_xet_available():
        if not has_buffered_io_data:
            _upload_xet_files(
                additions=additions,
                repo_type=repo_type,
                repo_id=repo_id,
                headers=headers,
                endpoint=endpoint,
                revision=revision,
                create_pr=create_pr,
            )
            return
        logger.warning(
            "Uploading files as a binary IO buffer is not supported by Xet Storage. Falling back to HTTP upload."
        )

    # Legacy LFS path: sha256 is required by the LFS batch endpoint => compute missing ones (in parallel).
    _compute_missing_sha256s(additions, num_threads=num_threads)

    lfs_actions: list[dict[str, Any]] = []
    lfs_oid2addop: dict[str, CommitOperationAdd] = {}
    for chunk in chunk_iterable(additions, chunk_size=UPLOAD_BATCH_MAX_NUM_FILES):
        chunk_list = [op for op in chunk]
        actions_chunk, errors_chunk, _ = post_lfs_batch_info(
            upload_infos=[op.upload_info for op in chunk_list],
            repo_id=repo_id,
            repo_type=repo_type,
            revision=revision,
            endpoint=endpoint,
            headers=headers,
            token=None,  # already passed in 'headers'
            transfers=["basic", "multipart"],
        )
        if errors_chunk:
            message = "\n".join(
                [
                    f"Encountered error for file with OID {err.get('oid')}: `{err.get('error', {}).get('message')}"
                    for err in errors_chunk
                ]
            )
            raise ValueError(f"LFS batch API returned errors:\n{message}")
        lfs_actions.extend(actions_chunk)
        for op in chunk_list:
            lfs_oid2addop[op.upload_info.sha256.hex()] = op

    if len(lfs_actions) > 0:
        _upload_lfs_files(
            actions=lfs_actions,
            oid2addop=lfs_oid2addop,
            headers=headers,
            endpoint=endpoint,
            num_threads=num_threads,
        )

