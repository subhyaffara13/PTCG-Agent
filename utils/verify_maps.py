from pathlib import Path


def verify_maps(
    *,
    remote_by_path: dict[str, "RepoFile"],
    local_by_path: dict[str, Path],
    revision: str,
    verified_path: Path,
) -> FolderVerification:
    """Compare remote entries and local files and return a verification result."""
    remote_paths = set(remote_by_path)
    local_paths = set(local_by_path)

    missing = sorted(remote_paths - local_paths)
    extra = sorted(local_paths - remote_paths)
    both = sorted(remote_paths & local_paths)

    mismatches: list[Mismatch] = []

    for rel_path in both:
        remote_entry = remote_by_path[rel_path]
        local_path = local_by_path[rel_path]

        lfs = getattr(remote_entry, "lfs", None)
        lfs_sha = getattr(lfs, "sha256", None) if lfs is not None else None
        if lfs_sha is None and isinstance(lfs, dict):
            lfs_sha = lfs.get("sha256")
        if lfs_sha:
            algorithm: HashAlgo = "sha256"
            expected = str(lfs_sha).lower()
        else:
            blob_id = remote_entry.blob_id  # type: ignore
            algorithm = "git-sha1"
            expected = str(blob_id).lower()

        actual = compute_file_hash(local_path, algorithm)

        if actual != expected:
            mismatches.append(Mismatch(path=rel_path, expected=expected, actual=actual, algorithm=algorithm))

    return FolderVerification(
        revision=revision,
        checked_count=len(both),
        mismatches=mismatches,
        missing_paths=missing,
        extra_paths=extra,
        verified_path=verified_path,
    )

