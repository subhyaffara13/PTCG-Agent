
def _log_audit_task_exception(task: "asyncio.Task[None]") -> None:
    """Surface a fire-and-forget audit-log task failure as a warning.

    ``asyncio.create_task`` swallows exceptions silently — if the audit
    write fails we'd otherwise lose the row without any signal.
    """
    if task.cancelled():
        return
    exc = task.exception()
    if exc is not None:
        verbose_proxy_logger.warning(
            "Failed to write cache-settings audit log: %s", exc
        )


def _log_audit_task_exception(task: "asyncio.Task[None]") -> None:
    if task.cancelled():
        return
    exc = task.exception()
    if exc is not None:
        verbose_proxy_logger.warning(
            "Failed to write hashicorp-vault config audit log: %s", exc
        )


def _log_audit_task_exception(task: "asyncio.Task[None]") -> None:
    """Surface a fire-and-forget audit-log task failure.

    ``asyncio.create_task`` swallows exceptions silently — if the audit
    write fails (transient DB error etc.) we'd otherwise lose the row
    without any signal.  Log at warning level so the operator sees there's
    a gap in the audit trail.
    """
    if task.cancelled():
        return
    exc = task.exception()
    if exc is not None:
        verbose_proxy_logger.warning("Failed to write team-callback audit log: %s", exc)

