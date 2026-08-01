
def _upload_parts_iteratively(
    operation: "CommitOperationAdd", sorted_parts_urls: list[str], chunk_size: int
) -> list[dict]:
    headers = []
    with operation.as_file(with_tqdm=True) as fileobj:
        for part_idx, part_upload_url in enumerate(sorted_parts_urls):
            with SliceFileObj(
                fileobj,
                seek_from=chunk_size * part_idx,
                read_limit=chunk_size,
            ) as fileobj_slice:
                # S3 might raise a transient 500 error -> let's retry if that happens
                part_upload_res = http_backoff("PUT", part_upload_url, data=fileobj_slice)
                hf_raise_for_status(part_upload_res)
                headers.append(part_upload_res.headers)
    return headers  # type: ignore

