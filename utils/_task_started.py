
def _task_started(task: asyncio.Task) -> bool:
    """Return ``True`` if the task has been started and has not finished."""
    # The task coro should never be None here, as we never add finished tasks to the
    # task list
    coro = task.get_coro()
    assert coro is not None
    return getcoroutinestate(coro) in (CORO_RUNNING, CORO_SUSPENDED)

