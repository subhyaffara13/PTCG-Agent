
def _reset_all_after_fork() -> None:  # pragma: no cover - fork child, not tracked by coverage
    global _all_instances_lock  # noqa: PLW0603
    # User-created threading locks do not auto-reset across fork: any lock held by a parent thread stays
    # locked in the child with no owner to release it. Replace the module-level lock and every instance's
    # locks with fresh ones; the child is single-threaded at this point so no synchronization is needed.
    _all_instances_lock = threading.Lock()
    for instance in list(_all_instances.values()):
        instance._reset_after_fork_in_child()  # noqa: SLF001

