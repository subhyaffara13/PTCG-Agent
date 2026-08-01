
def _compute_sync_plan(
    source: str,
    dest: str,
    api: "HfApi",
    delete: bool = False,
    ignore_times: bool = False,
    ignore_sizes: bool = False,
    existing: bool = False,
    ignore_existing: bool = False,
    filter_matcher: FilterMatcher | None = None,
    status: Any | None = None,
) -> SyncPlan:
    """Compute the sync plan by comparing source and destination.

    Returns:
        SyncPlan with all operations to be performed
    """
    filter_matcher = filter_matcher or FilterMatcher()
    is_upload = not _is_bucket_path(source) and _is_bucket_path(dest)
    is_download = _is_bucket_path(source) and not _is_bucket_path(dest)

    if not is_upload and not is_download:
        raise ValueError("One of source or dest must be a bucket path (hf://buckets/...) and the other must be local.")

    plan = SyncPlan(
        source=source,
        dest=dest,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    remote_total: int | None = None
    if is_upload:
        # Local -> Remote
        local_path = os.path.abspath(source)
        parsed = _parse_bucket_uri(dest)
        bucket_id, prefix = parsed.id, parsed.path_in_repo

        if not os.path.isdir(local_path):
            raise ValueError(f"Source must be a directory: {local_path}")

        # Get local and remote file lists
        local_files = {}
        for rel_path, size, mtime_ms in _list_local_files(local_path):
            if filter_matcher.matches(rel_path):
                local_files[rel_path] = (size, mtime_ms)
            if status:
                status.update(f"Scanning local directory ({len(local_files)} files)")
        if status:
            status.done(f"Scanning local directory ({len(local_files)} files)")

        remote_files = {}
        if status:
            try:
                remote_total = api.bucket_info(bucket_id).total_files
            except Exception:
                pass
        try:
            for rel_path, size, mtime_ms, _ in _list_remote_files(api, bucket_id, prefix):
                if filter_matcher.matches(rel_path):
                    remote_files[rel_path] = (size, mtime_ms)
                if status:
                    total_str = f"/{remote_total}" if remote_total is not None else ""
                    status.update(f"Scanning remote bucket ({len(remote_files)}{total_str} files)")
        except BucketNotFoundError:
            # Bucket doesn't exist yet - this is expected for new uploads
            logger.debug(f"Bucket '{bucket_id}' not found, treating as empty.")
        if status:
            status.done(f"Scanning remote bucket ({len(remote_files)} files)")

        # Compare files
        all_paths = set(local_files.keys()) | set(remote_files.keys())
        if status:
            status.done(f"Comparing files ({len(all_paths)} paths)")
        for path in sorted(all_paths):
            local_info = local_files.get(path)
            remote_info = remote_files.get(path)

            if local_info and not remote_info:
                # New file
                if existing:
                    # --existing: skip new files
                    plan.operations.append(
                        SyncOperation(
                            action="skip",
                            path=path,
                            size=local_info[0],
                            reason="new file (--existing)",
                            local_mtime=_mtime_to_iso(local_info[1]),
                        )
                    )
                else:
                    plan.operations.append(
                        SyncOperation(
                            action="upload",
                            path=path,
                            size=local_info[0],
                            reason="new file",
                            local_mtime=_mtime_to_iso(local_info[1]),
                        )
                    )
            elif local_info and remote_info:
                # File exists in both - use helper to determine action
                local_size, local_mtime = local_info
                remote_size, remote_mtime = remote_info
                plan.operations.append(
                    _compare_files_for_sync(
                        path=path,
                        action="upload",
                        source_size=local_size,
                        source_mtime=local_mtime,
                        dest_size=remote_size,
                        dest_mtime=remote_mtime,
                        source_newer_label="local newer",
                        dest_newer_label="remote newer",
                        ignore_sizes=ignore_sizes,
                        ignore_times=ignore_times,
                        ignore_existing=ignore_existing,
                    )
                )
            elif not local_info and remote_info and delete:
                # File only in remote and --delete mode
                plan.operations.append(
                    SyncOperation(
                        action="delete",
                        path=path,
                        size=remote_info[0],
                        reason="not in source (--delete)",
                        remote_mtime=_mtime_to_iso(remote_info[1]),
                    )
                )

    else:
        # Remote -> Local (download)
        parsed = _parse_bucket_uri(source)
        bucket_id, prefix = parsed.id, parsed.path_in_repo
        local_path = os.path.abspath(dest)

        # Get remote and local file lists
        remote_files = {}
        bucket_file_map: dict[str, Any] = {}
        if status:
            try:
                remote_total = api.bucket_info(bucket_id).total_files
            except Exception:
                pass
        for rel_path, size, mtime_ms, bucket_file in _list_remote_files(api, bucket_id, prefix):
            if filter_matcher.matches(rel_path):
                remote_files[rel_path] = (size, mtime_ms)
                bucket_file_map[rel_path] = bucket_file
            if status:
                total_str = f"/{remote_total}" if remote_total is not None else ""
                status.update(f"Scanning remote bucket ({len(remote_files)}{total_str} files)")
        if status:
            status.done(f"Scanning remote bucket ({len(remote_files)} files)")

        local_files = {}
        if os.path.isdir(local_path):
            if delete:
                # Full walk needed to discover local-only files for deletion.
                for rel_path, size, mtime_ms in _list_local_files(local_path):
                    if filter_matcher.matches(rel_path):
                        local_files[rel_path] = (size, mtime_ms)
                    if status:
                        status.update(f"Scanning local directory ({len(local_files)} files)")
            else:
                # Without --delete, the plan only depends on paths that exist
                # remotely. Stat just those instead of walking the whole tree,
                # which can take minutes when dest sits in a large directory
                # like ~/.cache/huggingface/.
                for rel_path in remote_files:
                    local_file = os.path.join(local_path, rel_path)
                    stat_info = _stat_local(local_file)
                    if stat_info is None:
                        continue
                    local_files[rel_path] = stat_info
                    if status:
                        status.update(f"Scanning local directory ({len(local_files)} files)")
        if status:
            status.done(f"Scanning local directory ({len(local_files)} files)")

        # Compare files
        all_paths = set(remote_files.keys()) | set(local_files.keys())
        if status:
            status.done(f"Comparing files ({len(all_paths)} paths)")
        for path in sorted(all_paths):
            remote_info = remote_files.get(path)
            local_info = local_files.get(path)

            if remote_info and not local_info:
                # New file
                if existing:
                    # --existing: skip new files
                    plan.operations.append(
                        SyncOperation(
                            action="skip",
                            path=path,
                            size=remote_info[0],
                            reason="new file (--existing)",
                            remote_mtime=_mtime_to_iso(remote_info[1]),
                        )
                    )
                else:
                    plan.operations.append(
                        SyncOperation(
                            action="download",
                            path=path,
                            size=remote_info[0],
                            reason="new file",
                            remote_mtime=_mtime_to_iso(remote_info[1]),
                            bucket_file=bucket_file_map.get(path),
                        )
                    )
            elif remote_info and local_info:
                # File exists in both - use helper to determine action
                remote_size, remote_mtime = remote_info
                local_size, local_mtime = local_info
                plan.operations.append(
                    _compare_files_for_sync(
                        path=path,
                        action="download",
                        source_size=remote_size,
                        source_mtime=remote_mtime,
                        dest_size=local_size,
                        dest_mtime=local_mtime,
                        source_newer_label="remote newer",
                        dest_newer_label="local newer",
                        ignore_sizes=ignore_sizes,
                        ignore_times=ignore_times,
                        ignore_existing=ignore_existing,
                        bucket_file=bucket_file_map.get(path),
                    )
                )
            elif not remote_info and local_info and delete:
                # File only in local and --delete mode
                plan.operations.append(
                    SyncOperation(
                        action="delete",
                        path=path,
                        size=local_info[0],
                        reason="not in source (--delete)",
                        local_mtime=_mtime_to_iso(local_info[1]),
                    )
                )

    return plan

