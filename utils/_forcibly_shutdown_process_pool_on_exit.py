import sys

def _forcibly_shutdown_process_pool_on_exit(
    workers: set[Process], _task: object
) -> None:
    """
    Forcibly shuts down worker processes belonging to this event loop."""
    child_watcher: asyncio.AbstractChildWatcher | None = None  # type: ignore[name-defined]
    if sys.version_info < (3, 12):
        try:
            child_watcher = asyncio.get_event_loop_policy().get_child_watcher()
        except NotImplementedError:
            pass

    # Close as much as possible (w/o async/await) to avoid warnings
    for process in workers.copy():
        if process.returncode is not None:
            continue

        process._stdin._stream._transport.close()  # type: ignore[union-attr]
        process._stdout._stream._transport.close()  # type: ignore[union-attr]
        process._stderr._stream._transport.close()  # type: ignore[union-attr]
        process.kill()
        if child_watcher:
            child_watcher.remove_child_handler(process.pid)

