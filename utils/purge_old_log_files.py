import os

def purge_old_log_files() -> None:
    """
    Purge the old log file at the beginning when the benchmark script runs.
    Should do it in the parent process rather than the child processes running
    each individual model.
    """
    for name, table in REGISTERED_METRIC_TABLES.items():
        if name in enabled_metric_tables():
            filename = table.output_filename()
            if os.path.exists(filename):
                os.unlink(filename)

            table.write_header()

