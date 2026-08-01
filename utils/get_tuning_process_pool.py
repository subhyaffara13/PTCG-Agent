
def get_tuning_process_pool() -> TuningProcessPool:
    pool = TuningProcessPool()
    atexit.register(pool.shutdown)
    return pool

