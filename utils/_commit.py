
def _commit(items: list[JOB_ITEM_T], api: "HfApi", repo_id: str, repo_type: str, revision: str) -> None:
    """Commit files to the repo."""
    additions = [_build_hacky_operation(item) for item in items]
    api.create_commit(
        repo_id=repo_id,
        repo_type=repo_type,
        revision=revision,
        operations=additions,
        commit_message="Add files using upload-large-folder tool",
    )
    for paths, metadata in items:
        metadata.is_committed = True
        metadata.save(paths)

