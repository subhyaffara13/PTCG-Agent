
def _upload_single(api: HfApi, uri: HfUri, source: str | bytes, remote_path: str) -> None:
    """Upload a single file or bytes (to a repo or bucket)."""
    if uri.is_bucket:
        api.batch_bucket_files(uri.id, add=[(source, remote_path)])
    else:
        api.upload_file(
            path_or_fileobj=source,
            path_in_repo=remote_path,
            repo_id=uri.id,
            repo_type=uri.type,
            revision=uri.revision,
        )

