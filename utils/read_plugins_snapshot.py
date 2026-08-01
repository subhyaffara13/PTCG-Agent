
def read_plugins_snapshot(manager: BuildManager) -> dict[str, str] | None:
    """Read cached snapshot of versions and hashes of plugins from previous run."""
    snapshot = _load_json_file(
        PLUGIN_SNAPSHOT_FILE,
        manager,
        log_success="Plugins snapshot (cached) ",
        log_error="Could not load plugins snapshot: ",
    )
    if snapshot is None:
        return None
    if not isinstance(snapshot, dict):
        manager.log(f"Could not load plugins snapshot: cache is not a dict: {type(snapshot)}")  # type: ignore[unreachable]
        return None
    return snapshot

