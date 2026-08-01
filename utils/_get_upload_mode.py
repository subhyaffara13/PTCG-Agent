
def _get_upload_mode(items: list[JOB_ITEM_T], api: "HfApi", repo_id: str, repo_type: str, revision: str) -> None:
    """Get upload mode for each file and update metadata.

    Also receive info if the file should be ignored.
    """
    additions = [_build_hacky_operation(item) for item in items]
    _fetch_upload_modes(
        additions=additions,
        repo_type=repo_type,
        repo_id=repo_id,
        headers=api._build_hf_headers(),
        revision=quote(revision, safe=""),
        endpoint=api.endpoint,
    )
    for item, addition in zip(items, additions):
        paths, metadata = item
        metadata.upload_mode = addition._upload_mode
        metadata.should_ignore = addition._should_ignore
        metadata.remote_oid = addition._remote_oid
        metadata.save(paths)

