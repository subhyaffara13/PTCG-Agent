
def lfs_upload(
    operation: "CommitOperationAdd",
    lfs_batch_action: dict,
    token: str | None = None,
    headers: dict[str, str] | None = None,
    endpoint: str | None = None,
) -> None:
    """
    Handles uploading a given object to the Hub with the LFS protocol.

    Can be a No-op if the content of the file is already present on the hub large file storage.

    Args:
        operation (`CommitOperationAdd`):
            The add operation triggering this upload.
        lfs_batch_action (`dict`):
            Upload instructions from the LFS batch endpoint for this object. See [`~utils.lfs.post_lfs_batch_info`] for
            more details.
        token (`str`, *optional*):
            An authentication token (see https://huggingface.co/settings/token). Used to call the
            optional LFS verify step at the end of the upload. If `None`, falls back to the local
            cached token.
        headers (`dict`, *optional*):
            Headers to include in the request, including authentication and user agent headers.
        endpoint (`str`, *optional*):
            The Hub endpoint to send the request to. Defaults to the value of `HF_ENDPOINT`.

    Raises:
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If `lfs_batch_action` is improperly formatted
        [`HfHubHTTPError`]
            If the upload resulted in an error
    """
    # 0. If LFS file is already present, skip upload
    _validate_batch_actions(lfs_batch_action)
    actions = lfs_batch_action.get("actions")
    if actions is None:
        # The file was already uploaded
        logger.debug(f"Content of file {operation.path_in_repo} is already present upstream - skipping upload")
        return

    # 1. Validate server response (check required keys in dict)
    upload_action = lfs_batch_action["actions"]["upload"]
    _validate_lfs_action(upload_action)
    verify_action = lfs_batch_action["actions"].get("verify")
    if verify_action is not None:
        _validate_lfs_action(verify_action)

    # 2. Upload file (either single part or multi-part)
    header = upload_action.get("header", {})
    chunk_size = header.get("chunk_size")
    upload_url = fix_hf_endpoint_in_url(upload_action["href"], endpoint=endpoint)
    if chunk_size is not None:
        try:
            chunk_size = int(chunk_size)
        except (ValueError, TypeError):
            raise ValueError(
                f"Malformed response from LFS batch endpoint: `chunk_size` should be an integer. Got '{chunk_size}'."
            )
        _upload_multi_part(operation=operation, header=header, chunk_size=chunk_size, upload_url=upload_url)
    else:
        _upload_single_part(operation=operation, upload_url=upload_url)

    # 3. Verify upload went well
    if verify_action is not None:
        _validate_lfs_action(verify_action)
        verify_url = fix_hf_endpoint_in_url(verify_action["href"], endpoint)
        verify_resp = http_backoff(
            "POST",
            verify_url,
            headers=build_hf_headers(token=token, headers=headers),
            json={"oid": operation.upload_info.sha256.hex(), "size": operation.upload_info.size},
        )
        hf_raise_for_status(verify_resp)
    logger.debug(f"{operation.path_in_repo}: Upload successful")

