
def _preupload_lfs(items: list[JOB_ITEM_T], api: "HfApi", repo_id: str, repo_type: str, revision: str) -> None:
    """Preupload LFS files and update metadata."""
    additions = [_build_hacky_operation(item) for item in items]
    api.preupload_lfs_files(
        repo_id=repo_id,
        repo_type=repo_type,
        revision=revision,
        additions=additions,
    )

    for paths, metadata in items:
        metadata.is_uploaded = True
        metadata.save(paths)

