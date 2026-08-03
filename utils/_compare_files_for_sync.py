from typing import Any

def _compare_files_for_sync(
    *,
    path: str,
    action: Literal["upload", "download"],
    source_size: int,
    source_mtime: float,
    dest_size: int,
    dest_mtime: float,
    source_newer_label: str,
    dest_newer_label: str,
    ignore_sizes: bool,
    ignore_times: bool,
    ignore_existing: bool,
    bucket_file: Any | None = None,
) -> SyncOperation:
    """Compare source and dest files and return the appropriate sync operation.

    This is a unified helper for both upload and download directions.

    Args:
        path: Relative file path
        action: "upload" or "download"
        source_size: Size of the source file (bytes)
        source_mtime: Mtime of the source file (milliseconds)
        dest_size: Size of the destination file (bytes)
        dest_mtime: Mtime of the destination file (milliseconds)
        source_newer_label: Label when source is newer (e.g., "local newer" or "remote newer")
        dest_newer_label: Label when dest is newer (e.g., "remote newer" or "local newer")
        ignore_sizes: Only compare mtime
        ignore_times: Only compare size
        ignore_existing: Skip files that exist on receiver
        bucket_file: BucketFile object (for downloads only)

    Returns:
        SyncOperation describing the action to take
    """
    local_mtime_iso = _mtime_to_iso(source_mtime if action == "upload" else dest_mtime)
    remote_mtime_iso = _mtime_to_iso(dest_mtime if action == "upload" else source_mtime)

    base_kwargs: dict[str, Any] = {
        "path": path,
        "size": source_size,
        "local_mtime": local_mtime_iso,
        "remote_mtime": remote_mtime_iso,
    }

    if ignore_existing:
        return SyncOperation(action="skip", reason="exists on receiver (--ignore-existing)", **base_kwargs)

    size_differs = source_size != dest_size
    source_newer = (source_mtime - dest_mtime) > _SYNC_TIME_WINDOW_MS

    if ignore_sizes:
        if source_newer:
            return SyncOperation(action=action, reason=source_newer_label, bucket_file=bucket_file, **base_kwargs)
        else:
            dest_newer = (dest_mtime - source_mtime) > _SYNC_TIME_WINDOW_MS
            skip_reason = dest_newer_label if dest_newer else "same mtime"
            return SyncOperation(action="skip", reason=skip_reason, **base_kwargs)
    elif ignore_times:
        if size_differs:
            return SyncOperation(action=action, reason="size differs", bucket_file=bucket_file, **base_kwargs)
        else:
            return SyncOperation(action="skip", reason="same size", **base_kwargs)
    else:
        if size_differs or source_newer:
            reason = "size differs" if size_differs else source_newer_label
            return SyncOperation(action=action, reason=reason, bucket_file=bucket_file, **base_kwargs)
        else:
            return SyncOperation(action="skip", reason="identical", **base_kwargs)

