
def _fetch_upload_modes(
    additions: Iterable[CommitOperationAdd],
    repo_type: str,
    repo_id: str,
    headers: dict[str, str],
    revision: str,
    endpoint: str | None = None,
    create_pr: bool = False,
    gitignore_content: str | None = None,
) -> None:
    """
    Requests the Hub "preupload" endpoint to determine whether each input file should be uploaded as a regular git blob,
    as a git LFS blob, or as a XET file. Input `additions` are mutated in-place with the upload mode.

    Args:
        additions (`Iterable` of :class:`CommitOperationAdd`):
            Iterable of :class:`CommitOperationAdd` describing the files to
            upload to the Hub.
        repo_type (`str`):
            Type of the repo to upload to: `"model"`, `"dataset"` or `"space"`.
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated
            by a `/`.
        headers (`dict[str, str]`):
            Headers to use for the request, including authorization headers and user agent.
        revision (`str`):
            The git revision to upload the files to. Can be any valid git revision.
        gitignore_content (`str`, *optional*):
            The content of the `.gitignore` file to know which files should be ignored. The order of priority
            is to first check if `gitignore_content` is passed, then check if the `.gitignore` file is present
            in the list of files to commit and finally default to the `.gitignore` file already hosted on the Hub
            (if any).
    Raises:
        [`~utils.HfHubHTTPError`]
            If the Hub API returned an error.
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If the Hub API response is improperly formatted.
    """
    endpoint = endpoint if endpoint is not None else constants.ENDPOINT

    # Fetch upload mode (LFS or regular) chunk by chunk.
    upload_modes: dict[str, UploadMode] = {}
    should_ignore_info: dict[str, bool] = {}
    oid_info: dict[str, str | None] = {}

    for chunk in chunk_iterable(additions, 256):
        payload: dict = {
            "files": [
                {
                    "path": op.path_in_repo,
                    "sample": base64.b64encode(op.upload_info.sample).decode("ascii"),
                    "size": op.upload_info.size,
                }
                for op in chunk
            ]
        }
        if gitignore_content is not None:
            payload["gitIgnore"] = gitignore_content

        resp = http_backoff(
            "POST",
            f"{endpoint}/api/{repo_type}s/{repo_id}/preupload/{revision}",
            json=payload,
            headers=headers,
            params={"create_pr": "1"} if create_pr else None,
        )
        hf_raise_for_status(resp)
        preupload_info = _validate_preupload_info(resp.json())
        upload_modes.update(**{file["path"]: file["uploadMode"] for file in preupload_info["files"]})
        should_ignore_info.update(**{file["path"]: file["shouldIgnore"] for file in preupload_info["files"]})
        oid_info.update(**{file["path"]: file.get("oid") for file in preupload_info["files"]})

    # Set upload mode for each addition operation
    for addition in additions:
        addition._upload_mode = upload_modes[addition.path_in_repo]
        addition._should_ignore = should_ignore_info[addition.path_in_repo]
        addition._remote_oid = oid_info[addition.path_in_repo]

    # Empty files cannot be uploaded as LFS (S3 would fail with a 501 Not Implemented)
    # => empty files are uploaded as "regular" to still allow users to commit them.
    for addition in additions:
        if addition.upload_info.size == 0:
            addition._upload_mode = "regular"

