
def _validate_upload_limits(paths_list: list[LocalUploadFilePaths]) -> None:
    """
    Validate upload against repository limits and warn about potential issues.

    Args:
        paths_list: List of file paths to be uploaded

    Warns about:
        - Too many files in the repository (>100k)
        - Too many entries (files or subdirectories) in a single folder (>10k)
        - Files exceeding size limits (>20GB recommended, >200GB maximum)
    """
    logger.info("Running validation checks on files to upload...")

    # Check 1: Total file count
    if len(paths_list) > MAX_FILES_PER_REPO:
        logger.warning(
            f"You are about to upload {len(paths_list):,} files. "
            f"This exceeds the recommended limit of {MAX_FILES_PER_REPO:,} files per repository.\n"
            f"Consider:\n"
            f"  - Splitting your data into multiple repositories\n"
            f"  - Using fewer, larger files (e.g., parquet files)\n"
            f"  - See: https://huggingface.co/docs/hub/repositories-recommendations"
        )

    # Check 2: Files and subdirectories per folder
    # Track immediate children (files and subdirs) for each folder
    from collections import defaultdict

    entries_per_folder: dict[str, Any] = defaultdict(lambda: {"files": 0, "subdirs": set()})

    for paths in paths_list:
        path = Path(paths.path_in_repo)
        parts = path.parts

        # Count this file in its immediate parent directory
        parent = str(path.parent) if str(path.parent) != "." else "."
        entries_per_folder[parent]["files"] += 1

        # Track immediate subdirectories for each parent folder
        # Walk through the path components to track parent-child relationships
        for i, child in enumerate(parts[:-1]):
            parent = "." if i == 0 else "/".join(parts[:i])
            entries_per_folder[parent]["subdirs"].add(child)

    # Check limits for each folder
    for folder, data in entries_per_folder.items():
        file_count = data["files"]
        subdir_count = len(data["subdirs"])
        total_entries = file_count + subdir_count

        if total_entries > MAX_FILES_PER_FOLDER:
            folder_display = "root" if folder == "." else folder
            logger.warning(
                f"Folder '{folder_display}' contains {total_entries:,} entries "
                f"({file_count:,} files and {subdir_count:,} subdirectories). "
                f"This exceeds the recommended {MAX_FILES_PER_FOLDER:,} entries per folder.\n"
                "Consider reorganising into sub-folders."
            )

    # Check 3: File sizes
    large_files = []
    very_large_files = []

    for paths in paths_list:
        size = paths.file_path.stat().st_size
        size_gb = size / 1_000_000_000  # Use decimal GB as per Hub limits

        if size_gb > MAX_FILE_SIZE_GB:
            very_large_files.append((paths.path_in_repo, size_gb))
        elif size_gb > RECOMMENDED_FILE_SIZE_GB:
            large_files.append((paths.path_in_repo, size_gb))

    # Warn about very large files (>200GB)
    if very_large_files:
        files_str = "\n  - ".join(f"{path}: {size:.1f}GB" for path, size in very_large_files[:5])
        more_str = f"\n  ... and {len(very_large_files) - 5} more files" if len(very_large_files) > 5 else ""
        logger.warning(
            f"Found {len(very_large_files)} files exceeding the {MAX_FILE_SIZE_GB}GB recommended maximum:\n"
            f"  - {files_str}{more_str}\n"
            f"Consider splitting these files into smaller chunks."
        )

    # Warn about large files (>20GB)
    if large_files:
        files_str = "\n  - ".join(f"{path}: {size:.1f}GB" for path, size in large_files[:5])
        more_str = f"\n  ... and {len(large_files) - 5} more files" if len(large_files) > 5 else ""
        logger.warning(
            f"Found {len(large_files)} files larger than {RECOMMENDED_FILE_SIZE_GB}GB (recommended limit):\n"
            f"  - {files_str}{more_str}\n"
            f"Large files may slow down loading and processing."
        )

    logger.info("Validation checks complete.")

