
def _upload_multi_part(operation: "CommitOperationAdd", header: dict, chunk_size: int, upload_url: str) -> None:
    """
    Uploads file using HF multipart LFS transfer protocol.
    """
    # 1. Get upload URLs for each part
    sorted_parts_urls = _get_sorted_parts_urls(header=header, upload_info=operation.upload_info, chunk_size=chunk_size)

    # 2. Upload parts (pure Python)
    response_headers = _upload_parts_iteratively(
        operation=operation, sorted_parts_urls=sorted_parts_urls, chunk_size=chunk_size
    )

    # 3. Send completion request
    # NOTE: `upload_url` is the Hub completion endpoint (not the S3 upload URLs).
    completion_res = http_backoff(
        "POST",
        upload_url,
        json=_get_completion_payload(response_headers, operation.upload_info.sha256.hex()),
        headers=LFS_HEADERS,
    )
    hf_raise_for_status(completion_res)

