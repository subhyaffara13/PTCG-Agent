import os
import sys

def sync_bucket_internal(
    source: str | None = None,
    dest: str | None = None,
    *,
    api: "HfApi",
    delete: bool = False,
    ignore_times: bool = False,
    ignore_sizes: bool = False,
    existing: bool = False,
    ignore_existing: bool = False,
    include: list[str] | None = None,
    exclude: list[str] | None = None,
    filter_from: str | None = None,
    plan: str | None = None,
    apply: str | None = None,
    dry_run: bool = False,
    verbose: bool = False,
    quiet: bool = False,
    token: bool | str | None = None,
) -> SyncPlan:
    """Sync files between a local directory and a bucket.

    This is equivalent to the ``hf buckets sync`` CLI command. One of ``source`` or ``dest`` must be a bucket path
    (``hf://buckets/...``) and the other must be a local directory path.

    Args:
        source (`str`, *optional*):
            Source path: local directory or ``hf://buckets/namespace/bucket_name(/prefix)``.
            Required unless using ``apply``.
        dest (`str`, *optional*):
            Destination path: local directory or ``hf://buckets/namespace/bucket_name(/prefix)``.
            Required unless using ``apply``.
        api ([`HfApi`]):
            The HfApi instance to use for API calls.
        delete (`bool`, *optional*, defaults to `False`):
            Delete destination files not present in source.
        ignore_times (`bool`, *optional*, defaults to `False`):
            Skip files only based on size, ignoring modification times.
        ignore_sizes (`bool`, *optional*, defaults to `False`):
            Skip files only based on modification times, ignoring sizes.
        existing (`bool`, *optional*, defaults to `False`):
            Skip creating new files on receiver (only update existing files).
        ignore_existing (`bool`, *optional*, defaults to `False`):
            Skip updating files that exist on receiver (only create new files).
        include (`list[str]`, *optional*):
            Include files matching patterns (fnmatch-style).
        exclude (`list[str]`, *optional*):
            Exclude files matching patterns (fnmatch-style).
        filter_from (`str`, *optional*):
            Path to a filter file with include/exclude rules.
        plan (`str`, *optional*):
            Save sync plan to this JSONL file instead of executing.
        apply (`str`, *optional*):
            Apply a previously saved plan file. When set, ``source`` and ``dest`` are not needed.
        dry_run (`bool`, *optional*, defaults to `False`):
            Print sync plan to stdout as JSONL without executing.
        verbose (`bool`, *optional*, defaults to `False`):
            Show detailed per-file operations.
        quiet (`bool`, *optional*, defaults to `False`):
            Suppress all output and progress bars.
        token (Union[bool, str, None], optional):
            A valid user access token. If not provided, the locally saved token will be used.

    Returns:
        [`SyncPlan`]: The computed (or loaded) sync plan.

    Raises:
        `ValueError`: If arguments are invalid (e.g., both paths are remote, conflicting options).

    Example:
        ```python
        >>> from huggingface_hub import HfApi
        >>> api = HfApi()

        # Upload local directory to bucket
        >>> api.sync_bucket("./data", "hf://buckets/username/my-bucket")

        # Download bucket to local directory
        >>> api.sync_bucket("hf://buckets/username/my-bucket", "./data")

        # Sync with delete and filtering
        >>> api.sync_bucket(
        ...     "./data",
        ...     "hf://buckets/username/my-bucket",
        ...     delete=True,
        ...     include=["*.safetensors"],
        ... )

        # Dry run: preview what would be synced
        >>> plan = api.sync_bucket("./data", "hf://buckets/username/my-bucket", dry_run=True)
        >>> plan.summary()
        {'uploads': 3, 'downloads': 0, 'deletes': 0, 'skips': 1, 'total_size': 4096}

        # Save plan for review, then apply
        >>> api.sync_bucket("./data", "hf://buckets/username/my-bucket", plan="sync-plan.jsonl")
        >>> api.sync_bucket(apply="sync-plan.jsonl")
        ```
    """
    # Build API with token if needed
    if token is not None:
        from .hf_api import HfApi

        api = HfApi(token=token)
    # --- Apply mode ---
    if apply:
        if source or dest:
            raise ValueError("Cannot specify source/dest when using apply.")
        if plan is not None:
            raise ValueError("Cannot specify both plan and apply.")
        if delete:
            raise ValueError("Cannot specify delete when using apply.")
        if ignore_times:
            raise ValueError("Cannot specify ignore_times when using apply.")
        if ignore_sizes:
            raise ValueError("Cannot specify ignore_sizes when using apply.")
        if include:
            raise ValueError("Cannot specify include when using apply.")
        if exclude:
            raise ValueError("Cannot specify exclude when using apply.")
        if filter_from:
            raise ValueError("Cannot specify filter_from when using apply.")
        if existing:
            raise ValueError("Cannot specify existing when using apply.")
        if ignore_existing:
            raise ValueError("Cannot specify ignore_existing when using apply.")
        if dry_run:
            raise ValueError("Cannot specify dry_run when using apply.")

        sync_plan = _load_plan(apply)
        status = StatusLine(enabled=not quiet)
        if not quiet:
            _print_plan_summary(sync_plan)
            print("Executing plan...")

        if quiet:
            disable_progress_bars()
        try:
            _execute_plan(sync_plan, api, verbose=verbose, status=status)
        finally:
            if quiet:
                enable_progress_bars()

        if not quiet:
            print("Sync completed.")

        return sync_plan

    # --- Normal mode ---
    if not source or not dest:
        raise ValueError("Both source and dest are required (unless using apply).")

    source_is_bucket = _is_bucket_path(source)
    dest_is_bucket = _is_bucket_path(dest)

    if source_is_bucket and dest_is_bucket:
        raise ValueError("Remote to remote sync is not supported. One path must be local.")

    if not source_is_bucket and not dest_is_bucket:
        raise ValueError("One of source or dest must be a bucket path (hf://buckets/...).")

    if ignore_times and ignore_sizes:
        raise ValueError("Cannot specify both ignore_times and ignore_sizes.")

    if existing and ignore_existing:
        raise ValueError("Cannot specify both existing and ignore_existing.")

    if dry_run and plan:
        raise ValueError("Cannot specify both dry_run and plan.")

    # Validate local path
    if source_is_bucket:
        if os.path.exists(dest) and not os.path.isdir(dest):
            raise ValueError(f"Destination must be a directory: {dest}")
    else:
        if not os.path.isdir(source):
            raise ValueError(f"Source must be an existing directory: {source}")

    # Build filter matcher
    filter_rules = None
    if filter_from:
        filter_rules = _parse_filter_file(filter_from)

    filter_matcher = FilterMatcher(
        include_patterns=include,
        exclude_patterns=exclude,
        filter_rules=filter_rules,
    )

    # Compute sync plan
    status = StatusLine(enabled=not quiet and not dry_run)
    sync_plan = _compute_sync_plan(
        source=source,
        dest=dest,
        api=api,
        delete=delete,
        ignore_times=ignore_times,
        ignore_sizes=ignore_sizes,
        existing=existing,
        ignore_existing=ignore_existing,
        filter_matcher=filter_matcher,
        status=status,
    )

    if dry_run:
        _write_plan(sync_plan, sys.stdout)
        return sync_plan

    if plan:
        _save_plan(sync_plan, plan)
        if not quiet:
            _print_plan_summary(sync_plan)
            print(f"Plan saved to: {plan}")
        return sync_plan

    # Execute plan
    if not quiet:
        _print_plan_summary(sync_plan)

    summary = sync_plan.summary()
    if summary["uploads"] == 0 and summary["downloads"] == 0 and summary["deletes"] == 0:
        if not quiet:
            print("Nothing to sync.")
        return sync_plan

    if not quiet:
        print("Syncing...")

    if quiet:
        disable_progress_bars()
    try:
        _execute_plan(sync_plan, api, verbose=verbose, status=status)
    finally:
        if quiet:
            enable_progress_bars()

    if not quiet:
        print("Sync completed.")

    return sync_plan

