
def _upload_single_part(operation: "CommitOperationAdd", upload_url: str) -> None:
    """
    Uploads `fileobj` as a single PUT HTTP request (basic LFS transfer protocol)

    Args:
        upload_url (`str`):
            The URL to PUT the file to.
        fileobj:
            The file-like object holding the data to upload.

    Raises:
        [`HfHubHTTPError`]
            If the upload resulted in an error.
    """
    with operation.as_file(with_tqdm=True) as fileobj:
        # S3 might raise a transient 500 error -> let's retry if that happens
        response = http_backoff("PUT", upload_url, data=fileobj)
        hf_raise_for_status(response)

