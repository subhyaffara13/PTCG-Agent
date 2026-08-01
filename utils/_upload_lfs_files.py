
def _upload_lfs_files(
    *,
    actions: list[dict[str, Any]],
    oid2addop: dict[str, CommitOperationAdd],
    headers: dict[str, str],
    endpoint: str | None = None,
    num_threads: int = 5,
):
    """
    Uploads the content of `additions` to the Hub using the large file storage protocol.

    Relevant external documentation:
        - LFS Batch API: https://github.com/git-lfs/git-lfs/blob/main/docs/api/batch.md

    Args:
        actions (`list[dict[str, Any]]`):
            LFS batch actions returned by the server.
        oid2addop (`dict[str, CommitOperationAdd]`):
            A dictionary mapping the OID of the file to the corresponding `CommitOperationAdd` object.
        headers (`dict[str, str]`):
            Headers to use for the request, including authorization headers and user agent.
        endpoint (`str`, *optional*):
            The endpoint to use for the request. Defaults to `constants.ENDPOINT`.
        num_threads (`int`, *optional*):
            The number of concurrent threads to use when uploading. Defaults to 5.

    Raises:
        [`EnvironmentError`](https://docs.python.org/3/library/exceptions.html#EnvironmentError)
            If an upload failed for any reason
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            Type of the repo to upload to: `"model"`, `"dataset"` or `"space"`.
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated
            by a `/`.
        headers (`dict[str, str]`):
            Headers to use for the request, including authorization headers and user agent.
        num_threads (`int`, *optional*):
            The number of concurrent threads to use when uploading. Defaults to 5.
        revision (`str`, *optional*):
            The git revision to upload to.

    Raises:
        [`EnvironmentError`](https://docs.python.org/3/library/exceptions.html#EnvironmentError)
            If an upload failed for any reason
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If the server returns malformed responses
        [`HfHubHTTPError`]
            If the LFS batch endpoint returned an HTTP error.
    """
    # Filter out files already present upstream
    filtered_actions = []
    for action in actions:
        if action.get("actions") is None:
            logger.debug(
                f"Content of file {oid2addop[action['oid']].path_in_repo} is already present upstream - skipping upload."
            )
        else:
            filtered_actions.append(action)

    # Upload according to server-provided actions
    def _wrapped_lfs_upload(batch_action) -> None:
        try:
            operation = oid2addop[batch_action["oid"]]
            lfs_upload(operation=operation, lfs_batch_action=batch_action, headers=headers, endpoint=endpoint)
        except Exception as exc:
            raise RuntimeError(f"Error while uploading '{operation.path_in_repo}' to the Hub.") from exc

    if len(filtered_actions) == 1:
        logger.debug("Uploading 1 LFS file to the Hub")
        _wrapped_lfs_upload(filtered_actions[0])
    else:
        logger.debug(
            f"Uploading {len(filtered_actions)} LFS files to the Hub using up to {num_threads} threads concurrently"
        )
        thread_map(
            _wrapped_lfs_upload,
            filtered_actions,
            desc=f"Upload {len(filtered_actions)} LFS files",
            max_workers=num_threads,
            tqdm_class=hf_tqdm,
        )

