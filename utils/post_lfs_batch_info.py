
def post_lfs_batch_info(
    upload_infos: Iterable[UploadInfo],
    token: str | None,
    repo_type: str,
    repo_id: str,
    revision: str | None = None,
    endpoint: str | None = None,
    headers: dict[str, str] | None = None,
    transfers: list[str] | None = None,
) -> tuple[list[dict], list[dict], str | None]:
    """
    Requests the LFS batch endpoint to retrieve upload instructions

    Learn more: https://github.com/git-lfs/git-lfs/blob/main/docs/api/batch.md

    Args:
        upload_infos (`Iterable` of `UploadInfo`):
            `UploadInfo` for the files that are being uploaded, typically obtained
            from `CommitOperationAdd.upload_info`
        token (`str` or `None`):
            An authentication token (see https://huggingface.co/settings/token).
            Pass `None` to fall back to the local cached token (or no token if unauthenticated).
        repo_type (`str`):
            Type of the repo to upload to: `"model"`, `"dataset"` or `"space"`.
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated
            by a `/`.
        revision (`str`, *optional*):
            The git revision to upload to.
        endpoint (`str`, *optional*):
            The Hub endpoint to send the request to. Defaults to the value of `HF_ENDPOINT`.
        headers (`dict`, *optional*):
            Additional headers to include in the request
        transfers (`list`, *optional*):
            List of transfer methods to use. Defaults to ["basic", "multipart"].

    Returns:
        `LfsBatchInfo`: 3-tuple:
            - First element is the list of upload instructions from the server
            - Second element is a list of errors, if any
            - Third element is the chosen transfer adapter if provided by the server (e.g. "basic", "multipart", "xet")

    Raises:
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If an argument is invalid or the server response is malformed.
        [`HfHubHTTPError`]
            If the server returned an error.
    """
    endpoint = endpoint if endpoint is not None else constants.ENDPOINT
    url_prefix = ""
    if repo_type in constants.REPO_TYPES_URL_PREFIXES:
        url_prefix = constants.REPO_TYPES_URL_PREFIXES[repo_type]
    batch_url = f"{endpoint}/{url_prefix}{repo_id}.git/info/lfs/objects/batch"
    payload: dict = {
        "operation": "upload",
        "transfers": transfers if transfers is not None else ["basic", "multipart"],
        "objects": [
            {
                "oid": upload.sha256.hex(),
                "size": upload.size,
            }
            for upload in upload_infos
        ],
        "hash_algo": "sha256",
    }
    if revision is not None:
        payload["ref"] = {"name": unquote(revision)}  # revision has been previously 'quoted'

    headers = {
        **LFS_HEADERS,
        **build_hf_headers(token=token),
        **(headers or {}),
    }
    resp = http_backoff("POST", batch_url, headers=headers, json=payload)
    hf_raise_for_status(resp)
    batch_info = resp.json()

    objects = batch_info.get("objects", None)
    if not isinstance(objects, list):
        raise ValueError("Malformed response from server")

    chosen_transfer = batch_info.get("transfer")
    chosen_transfer = chosen_transfer if isinstance(chosen_transfer, str) else None

    return (
        [_validate_batch_actions(obj) for obj in objects if "error" not in obj],
        [_validate_batch_error(obj) for obj in objects if "error" in obj],
        chosen_transfer,
    )

