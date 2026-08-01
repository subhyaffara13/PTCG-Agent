
def _cleanup_all_instances() -> None:  # pragma: no cover - runs from atexit at interpreter shutdown
    for instance in list(_all_instances.values()):
        with suppress(Exception):
            instance.release(force=True)

