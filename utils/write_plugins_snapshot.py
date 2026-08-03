import os

def write_plugins_snapshot(manager: BuildManager) -> None:
    """Write snapshot of versions and hashes of currently active plugins."""
    snapshot = json_dumps(manager.plugins_snapshot)
    if (
        not manager.metastore.write(PLUGIN_SNAPSHOT_FILE, snapshot)
        and manager.options.cache_dir != os.devnull
    ):
        manager.errors.set_file(_cache_dir_prefix(manager.options), None, manager.options)
        manager.error(None, "Error writing plugins snapshot", blocker=True)

