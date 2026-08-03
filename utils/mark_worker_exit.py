import os

def mark_worker_exit(worker_pid: int) -> None:
    """Remove prometheus .db files for a dead worker. Called by gunicorn child_exit hook."""
    if not os.environ.get("PROMETHEUS_MULTIPROC_DIR"):
        return
    try:
        from prometheus_client import multiprocess

        multiprocess.mark_process_dead(worker_pid)
        verbose_proxy_logger.info(
            f"Prometheus cleanup: marked worker {worker_pid} as dead"
        )
    except Exception as e:
        verbose_proxy_logger.warning(
            f"Failed to mark prometheus worker {worker_pid} as dead: {e}"
        )

