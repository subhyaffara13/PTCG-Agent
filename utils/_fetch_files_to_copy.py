from typing import Union

def _fetch_files_to_copy(
    copies: Iterable[CommitOperationCopy],
    repo_type: str,
    repo_id: str,
    headers: dict[str, str],
    revision: str,
    endpoint: str | None = None,
) -> dict[_CopySource, Union["RepoFile", bytes]]:
    """
    Fetch information about the files to copy.

    For LFS files, we only need their metadata (file size and sha256) while for regular files
    we need to download the raw content from the Hub.

    Args:
        copies (`Iterable` of :class:`CommitOperationCopy`):
            Iterable of :class:`CommitOperationCopy` describing the files to
            copy on the Hub.
        repo_type (`str`):
            Type of the repo to upload to: `"model"`, `"dataset"` or `"space"`.
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated
            by a `/`.
        headers (`dict[str, str]`):
            Headers to use for the request, including authorization headers and user agent.
        revision (`str`):
            The git revision to upload the files to. Can be any valid git revision.

    Returns: `dict[_CopySource, Union[RepoFile, bytes]]]`
        Key is `(src_repo_id, src_repo_type, path, revision)`. For intra-repo copies,
        `src_repo_id` and `src_repo_type` are `None`.
        Value is the raw content as bytes (for regular files) or the file information as a RepoFile (for LFS files).

    Raises:
        [`~utils.HfHubHTTPError`]
            If the Hub API returned an error.
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If the Hub API response is improperly formatted.
    """
    from .hf_api import HfApi, RepoFolder

    hf_api = HfApi(endpoint=endpoint, headers=headers)
    copies = list(copies)
    files_to_copy: dict[_CopySource, Union["RepoFile", bytes]] = {}
    oid_info: dict[tuple[str, str | None], str | None] = {}

    # 1. Fetch OIDs for destination paths in batches.
    dest_paths = [op.path_in_repo for op in copies]
    for batch in chunk_iterable(dest_paths, FETCH_LFS_BATCH_SIZE):
        dest_repo_files = hf_api.get_paths_info(
            repo_id=repo_id,
            paths=list(batch),
            revision=revision,
            repo_type=repo_type,
        )
        for file in dest_repo_files:
            if not isinstance(file, RepoFolder):
                oid_info[(file.path, revision)] = file.blob_id

    # 2. Fetch source file info, grouped by (src_repo_id, src_repo_type, src_revision).
    copies.sort(key=lambda op: (op.src_repo_id or "", op.src_repo_type or "", op.src_revision or ""))
    for (src_repo_id_key, src_repo_type_key, src_revision_key), group in groupby(
        copies, key=lambda op: (op.src_repo_id, op.src_repo_type, op.src_revision)
    ):
        operations = list(group)
        is_cross_repo = src_repo_id_key is not None
        eff_repo_id = src_repo_id_key or repo_id
        eff_repo_type = src_repo_type_key or repo_type
        eff_revision = src_revision_key or ("main" if is_cross_repo else revision)

        src_paths = [op.src_path_in_repo for op in operations]
        for paths_batch in chunk_iterable(src_paths, FETCH_LFS_BATCH_SIZE):
            src_repo_files = hf_api.get_paths_info(
                repo_id=eff_repo_id,
                paths=list(paths_batch),
                revision=eff_revision,
                repo_type=eff_repo_type,
            )
            for src_repo_file in src_repo_files:
                if isinstance(src_repo_file, RepoFolder):
                    raise NotImplementedError("Copying a folder is not implemented.")
                source = _CopySource(src_repo_id_key, src_repo_type_key, src_repo_file.path, src_revision_key)
                if src_repo_file.lfs:
                    files_to_copy[source] = src_repo_file
                else:
                    url = hf_hub_url(
                        endpoint=endpoint,
                        repo_type=eff_repo_type,
                        repo_id=eff_repo_id,
                        revision=eff_revision,
                        filename=src_repo_file.path,
                    )
                    response = get_session().get(url, headers=headers)
                    hf_raise_for_status(response)
                    files_to_copy[source] = response.content
                if not is_cross_repo:
                    oid_info[(src_repo_file.path, src_revision_key)] = src_repo_file.blob_id

        for operation in operations:
            key = _CopySource(src_repo_id_key, src_repo_type_key, operation.src_path_in_repo, src_revision_key)
            if key not in files_to_copy:
                source_desc = f" from {eff_repo_type}s/{eff_repo_id}" if is_cross_repo else ""
                raise EntryNotFoundError(
                    f"Cannot copy {operation.src_path_in_repo} at revision "
                    f"{eff_revision}{source_desc}: file is missing on repo."
                )
            operation._dest_oid = oid_info.get((operation.path_in_repo, revision))
            if not is_cross_repo:
                operation._src_oid = oid_info.get((operation.src_path_in_repo, operation.src_revision))

    return files_to_copy

