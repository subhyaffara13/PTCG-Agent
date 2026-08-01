
def _build_hacky_operation(item: JOB_ITEM_T) -> HackyCommitOperationAdd:
    paths, metadata = item
    operation = HackyCommitOperationAdd(path_in_repo=paths.path_in_repo, path_or_fileobj=paths.file_path)
    with paths.file_path.open("rb") as file:
        sample = file.peek(512)[:512]
    if metadata.sha256 is None:
        raise ValueError("sha256 must have been computed by now!")
    operation.upload_info = UploadInfo(sha256=bytes.fromhex(metadata.sha256), size=metadata.size, sample=sample)
    operation._upload_mode = metadata.upload_mode  # type: ignore
    operation._should_ignore = metadata.should_ignore
    operation._remote_oid = metadata.remote_oid
    operation._is_uploaded = metadata.is_uploaded
    if metadata.is_uploaded and metadata.upload_mode == "lfs":
        operation.path_or_fileobj = b""
    return operation

