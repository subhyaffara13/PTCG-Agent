
def _compute_missing_sha256s(additions: list[CommitOperationAdd], num_threads: int) -> None:
    """Compute the sha256 of the operations that don't have one yet, in parallel."""
    not_hashed = [op for op in additions if not op.upload_info.is_hashed]
    if len(not_hashed) == 0:
        return
    logger.info(f"Computing sha256 for {len(not_hashed)} files.")
    if len(not_hashed) == 1:
        _ = not_hashed[0].upload_info.sha256
        return
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        list(executor.map(lambda op: op.upload_info.sha256, not_hashed))

