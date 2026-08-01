
def pipelined_upload(
    api: "HfApi",
    *,
    repo_id: str,
    repo_type: str,
    add_operations: list[CommitOperationAdd],
    delete_operations: list[CommitOperationDelete],
    commit_message: str,
    commit_description: str | None = None,
    token: str | bool | None = None,
    revision: str | None = None,
    create_pr: bool = False,
    parent_commit: str | None = None,
) -> "CommitInfo":
    """Upload a prepared list of operations through the streamed multi-commit pipeline.

    Requires `hf_xet` to be installed. See module docstring for the architecture.
    """

    return _UploadPipeline(
        api,
        repo_id=repo_id,
        repo_type=repo_type,
        add_operations=add_operations,
        delete_operations=delete_operations,
        commit_message=commit_message,
        commit_description=commit_description,
        token=token,
        revision=revision,
        create_pr=create_pr,
        parent_commit=parent_commit,
    ).run()

