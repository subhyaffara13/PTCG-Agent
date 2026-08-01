
def _stop_workers(workers: deque[_Worker]) -> None:
    for worker in workers:
        worker.destroy()

    workers.clear()

