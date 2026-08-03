import os

def _download_single(api: HfApi, uri: HfUri, local_path: str) -> None:
    """Download a single file (repo or bucket) to ``local_path``.

    Used by `_download_file_to_local` and `_download_file_to_stdout`.
    """
    if uri.is_bucket:
        api.download_bucket_files(uri.id, [(uri.path_in_repo, local_path)], raise_on_missing_files=True)
    else:
        # Download into a temporary folder next to the destination (rather than the shared cache)
        # so the final move stays on the same filesystem and is instant. The temp folder is
        # cleaned up automatically once the move is complete.
        parent_dir = os.path.dirname(local_path) or "."
        with SoftTemporaryDirectory(prefix=".tmp", dir=parent_dir) as tmp_dir:
            downloaded_path = api.hf_hub_download(
                repo_id=uri.id,
                repo_type=uri.type,
                filename=uri.path_in_repo,
                revision=uri.revision,
                local_dir=tmp_dir,
            )
            os.replace(downloaded_path, local_path)

