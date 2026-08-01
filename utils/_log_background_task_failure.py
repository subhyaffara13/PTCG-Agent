
def _log_background_task_failure(task: "asyncio.Task[Any]", *, task_name: str) -> None:
    if task.cancelled():
        return
    exception = task.exception()
    if exception is not None:
        verbose_logger.error("%s failed: %s", task_name, exception)

