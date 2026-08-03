from pathlib import Path


def resolve_local_root(
    *,
    repo_id: str,
    repo_type: str,
    revision: str | None,
    cache_dir: Path | None,
    local_dir: Path | None,
) -> tuple[Path, str]:
    """
    Resolve the root directory to scan locally and the remote revision to verify.
    """
    if local_dir is not None:
        root = Path(local_dir).expanduser().resolve()
        if not root.is_dir():
            raise ValueError(f"Local directory does not exist or is not a directory: {root}")
        return root, (revision or constants.DEFAULT_REVISION)

    cache_root = Path(cache_dir or constants.HF_HUB_CACHE).expanduser().resolve()
    storage_folder = cache_root / repo_folder_name(repo_id=repo_id, repo_type=repo_type)
    if not storage_folder.exists():
        raise ValueError(
            f"Repo is not present in cache: {storage_folder}. Use 'hf download' first or pass --local-dir."
        )
    commit = _resolve_commit_hash_from_cache(storage_folder, revision)
    snapshot_dir = storage_folder / "snapshots" / commit
    if not snapshot_dir.is_dir():
        raise ValueError(f"Snapshot directory does not exist for revision '{commit}': {snapshot_dir}.")
    return snapshot_dir, commit

