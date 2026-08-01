
def _monitor_thread_target(
    status_dir: str, csv_path: Path, total: int,
    stop_event: threading.Event, overall_start: float,
    interval: float,
) -> None:
    while not stop_event.wait(interval):
        try:
            _print_snapshot(status_dir, csv_path, total, overall_start)
        except Exception as e:  # noqa: BLE001
            _log.warning("monitor snapshot failed: %s", e)

