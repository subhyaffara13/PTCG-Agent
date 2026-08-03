import time

def _load_ff_file(
    file: str, manager: BuildManager, log_error_fmt: str, id: str | None
) -> bytes | None:
    if manager.stats_enabled:
        t0 = time.time()
    try:
        data = manager.metastore.read(file)
    except OSError:
        if manager.logging_enabled:
            if id:
                message = log_error_fmt.format(id) + file
            else:
                message = log_error_fmt + file
            manager.log(message)
        return None
    if manager.stats_enabled:
        manager.add_stats(metastore_read_time=time.time() - t0)
    return data

