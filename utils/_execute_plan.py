
def _execute_plan(plan: SyncPlan, api: "HfApi", verbose: bool = False, status: Any | None = None) -> None:
    """Execute a sync plan."""
    is_upload = not _is_bucket_path(plan.source) and _is_bucket_path(plan.dest)
    is_download = _is_bucket_path(plan.source) and not _is_bucket_path(plan.dest)

    if is_upload:
        local_path = os.path.abspath(plan.source)
        parsed = _parse_bucket_uri(plan.dest)
        bucket_id, prefix = parsed.id, parsed.path_in_repo

        # Collect operations
        add_files: list[tuple[str | Path | bytes, str]] = []
        delete_paths: list[str] = []

        for op in plan.operations:
            match op.action:
                case "upload":
                    local_file = os.path.join(local_path, op.path)
                    remote_path = f"{prefix}/{op.path}" if prefix else op.path
                    if verbose:
                        print(f"  Uploading: {op.path} ({op.reason})")
                    add_files.append((local_file, remote_path))
                case "delete":
                    remote_path = f"{prefix}/{op.path}" if prefix else op.path
                    if verbose:
                        print(f"  Deleting: {op.path} ({op.reason})")
                    delete_paths.append(remote_path)
                case "skip" if verbose:
                    print(f"  Skipping: {op.path} ({op.reason})")

        # Execute batch operations
        if add_files or delete_paths:
            if status:
                parts = []
                if add_files:
                    parts.append(f"uploading {len(add_files)} files")
                if delete_paths:
                    parts.append(f"deleting {len(delete_paths)} files")
                status.done(", ".join(parts).capitalize())
            api.batch_bucket_files(
                bucket_id,
                add=add_files or None,
                delete=delete_paths or None,
            )

    elif is_download:
        parsed = _parse_bucket_uri(plan.source)
        bucket_id, prefix = parsed.id, parsed.path_in_repo
        local_path = os.path.abspath(plan.dest)

        # Ensure local directory exists
        os.makedirs(local_path, exist_ok=True)

        # Collect download operations
        download_files: list[tuple[str | BucketFile, str | Path]] = []
        delete_files: list[str] = []

        for op in plan.operations:
            if op.action == "download":
                local_file = os.path.join(local_path, op.path)
                # Ensure parent directory exists
                os.makedirs(os.path.dirname(local_file), exist_ok=True)
                if verbose:
                    print(f"  Downloading: {op.path} ({op.reason})")
                # Use BucketFile when available (avoids extra metadata fetch per file)
                if op.bucket_file is not None:
                    download_files.append((op.bucket_file, local_file))
                else:
                    remote_path = f"{prefix}/{op.path}" if prefix else op.path
                    download_files.append((remote_path, local_file))
            elif op.action == "delete":
                local_file = os.path.join(local_path, op.path)
                if verbose:
                    print(f"  Deleting: {op.path} ({op.reason})")
                delete_files.append(local_file)
            elif op.action == "skip" and verbose:
                print(f"  Skipping: {op.path} ({op.reason})")

        # Execute downloads
        if len(download_files) > 0:
            if status:
                status.done(f"Downloading {len(download_files)} files")
            api.download_bucket_files(bucket_id, download_files)

        # Execute deletes
        if status and delete_files:
            status.done(f"Deleting {len(delete_files)} local files")
        for file_path in delete_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                # Remove empty parent directories
                parent = os.path.dirname(file_path)
                while parent != local_path:
                    try:
                        os.rmdir(parent)
                        parent = os.path.dirname(parent)
                    except OSError:
                        break

