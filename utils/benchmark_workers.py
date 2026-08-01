
def benchmark_workers(a_bench_func=None, the_data=None):
    """does a little test to see if workers are at all faster.
    Returns the number of workers which works best.
    Takes a little bit of time to run, so you should only really call
      it once.
    You can pass in benchmark data, and functions if you want.
    a_bench_func - f(data)
    the_data - data to work on.
    """
    # TODO: try and make this scale better with slower/faster cpus.
    #  first find some variables so that using 0 workers takes about 1.0 seconds.
    #  then go from there.

    # note, this will only work with pygame 1.8rc3+
    # replace the doit() and the_data with something that releases the GIL

    import pygame
    import pygame.transform
    import time

    if not a_bench_func:

        def doit(x):
            return pygame.transform.scale(x, (544, 576))

    else:
        doit = a_bench_func

    if not the_data:
        thedata = [pygame.Surface((155, 155), 0, 32) for x in range(10)]
    else:
        thedata = the_data

    best = time.time() + 100000000
    best_number = 0
    # last_best = -1

    for num_workers in range(0, MAX_WORKERS_TO_TEST):
        wq = WorkerQueue(num_workers)
        t1 = time.time()
        for _ in range(20):
            print(f"active count:{threading.active_count()}")
            tmap(doit, thedata, worker_queue=wq)
        t2 = time.time()

        wq.stop()

        total_time = t2 - t1
        print(f"total time num_workers:{num_workers}: time:{total_time}:")

        if total_time < best:
            # last_best = best_number
            best_number = num_workers
            best = total_time

        if num_workers - best_number > 1:
            # We tried to add more, but it didn't like it.
            #   so we stop with testing at this number.
            break

    return best_number

