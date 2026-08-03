import os
import time
from pathlib import Path


def upload_large_folder_internal(
    api: "HfApi",
    repo_id: str,
    folder_path: str | Path,
    *,
    repo_type: str,  # Repo type is required!
    revision: str | None = None,
    private: bool | None = None,
    allow_patterns: list[str] | str | None = None,
    ignore_patterns: list[str] | str | None = None,
    num_workers: int | None = None,
    print_report: bool = True,
    print_report_every: int = 60,
):
    """Upload a large folder to the Hub in the most resilient way possible.

    See [`HfApi.upload_large_folder`] for the full documentation.
    """
    # 1. Check args and setup
    if repo_type is None:
        raise ValueError(
            "For large uploads, `repo_type` is explicitly required. Please set it to `model`, `dataset` or `space`."
            " If you are using the CLI, pass it as `--repo-type=model`."
        )
    if repo_type not in REPO_TYPES:
        raise ValueError(f"Invalid repo type, must be one of {REPO_TYPES}")
    if revision is None:
        revision = DEFAULT_REVISION

    folder_path = Path(folder_path).expanduser().resolve()
    if not folder_path.is_dir():
        raise ValueError(f"Provided path: '{folder_path}' is not a directory")

    if ignore_patterns is None:
        ignore_patterns = []
    elif isinstance(ignore_patterns, str):
        ignore_patterns = [ignore_patterns]
    ignore_patterns += DEFAULT_IGNORE_PATTERNS

    if num_workers is None:
        nb_cores = os.cpu_count() or 1
        num_workers = max(nb_cores // 2, 1)  # Use at most half of cpu cores

    # 2. Create repo if missing
    repo_url = api.create_repo(repo_id=repo_id, repo_type=repo_type, private=private, exist_ok=True)
    logger.info(f"Repo created: {repo_url}")
    repo_id = repo_url.repo_id

    # Warn on too many commits
    try:
        commits = api.list_repo_commits(repo_id=repo_id, repo_type=repo_type, revision=revision)
        commit_count = len(commits)
        if commit_count > 500:
            logger.warning(
                f"\n{'=' * 80}\n"
                f"WARNING: This repository has {commit_count} commits.\n"
                f"Repositories with a large number of commits can experience performance issues.\n"
                f"\n"
                f"Consider squashing your commit history using `super_squash_history()`.\n"
                "To do so, you need to stop this process, run the snippet below and restart the upload command."
                f"  from huggingface_hub import super_squash_history\n"
                f"  super_squash_history(repo_id='{repo_id}', repo_type='{repo_type}')\n"
                f"\n"
                f"Note: This is a non-revertible operation. See the documentation for more details:\n"
                f"https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#huggingface_hub.HfApi.super_squash_history\n"
                f"{'=' * 80}\n"
            )
    except Exception as e:
        # Don't fail the upload if we can't check commit count
        logger.debug(f"Could not check commit count: {e}")

    # 2.1 Check if xet is enabled to set batch file upload size
    upload_batch_size = UPLOAD_BATCH_SIZE_XET if is_xet_available() else UPLOAD_BATCH_SIZE_LFS

    # 3. List files to upload
    filtered_paths_list = filter_repo_objects(
        (path.relative_to(folder_path).as_posix() for path in folder_path.glob("**/*") if path.is_file()),
        allow_patterns=allow_patterns,
        ignore_patterns=ignore_patterns,
    )
    paths_list = [get_local_upload_paths(folder_path, relpath) for relpath in filtered_paths_list]
    logger.info(f"Found {len(paths_list)} candidate files to upload")

    # Validate upload against repository limits
    _validate_upload_limits(paths_list)

    logger.info("Starting upload...")

    # Read metadata for each file
    items = [
        (paths, read_upload_metadata(folder_path, paths.path_in_repo))
        for paths in tqdm(paths_list, desc="Recovering from metadata files")
    ]

    # 4. Start workers
    status = LargeUploadStatus(items, upload_batch_size)
    threads = [
        threading.Thread(
            target=_worker_job,
            kwargs={
                "status": status,
                "api": api,
                "repo_id": repo_id,
                "repo_type": repo_type,
                "revision": revision,
            },
        )
        for _ in range(num_workers)
    ]

    for thread in threads:
        thread.start()

    # 5. Print regular reports
    if print_report:
        print("\n\n" + status.current_report())
    last_report_ts = time.time()
    while True:
        time.sleep(1)
        if time.time() - last_report_ts >= print_report_every:
            if print_report:
                _print_overwrite(status.current_report())
            last_report_ts = time.time()
        if status.is_done():
            logger.info("Is done: exiting main loop")
            break

    for thread in threads:
        thread.join()

    logger.info(status.current_report())
    logger.info("Upload is complete!")

