
def _try_initialize_processpool(
    job_count: int,
    argv: Sequence[str],
) -> multiprocessing.pool.Pool | None:
    """Return a new process pool instance if we are able to create one."""
    try:
        return multiprocessing.Pool(job_count, _mp_init, initargs=(argv,))
    except OSError as err:
        if err.errno not in SERIAL_RETRY_ERRNOS:
            raise
    except ImportError:
        pass

    return None

