
def _audit_log_task_done_callback(task: asyncio.Task) -> None:
    """Log exceptions from audit log callback tasks so they don't slip through silently."""
    try:
        exc = task.exception()
    except asyncio.CancelledError:
        return
    if exc is not None:
        verbose_proxy_logger.error(
            "Audit log callback task failed: %s", exc, exc_info=exc
        )

