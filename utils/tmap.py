
def tmap(function, *sequences, **tqdm_kwargs):
    """
    Equivalent of builtin `map`.

    Parameters
    ----------
    tqdm_class  : [default: tqdm.auto.tqdm].
    """
    for i in tzip(*sequences, **tqdm_kwargs):
        yield function(*i)


def tmap(f, seq_args, num_workers=20, worker_queue=None, wait=True, stop_on_error=True):
    """like map, but uses a thread pool to execute.
    num_workers - the number of worker threads that will be used.  If pool
                    is passed in, then the num_workers arg is ignored.
    worker_queue - you can optionally pass in an existing WorkerQueue.
    wait - True means that the results are returned when everything is finished.
           False means that we return the [worker_queue, results] right away instead.
           results, is returned as a list of FuncResult instances.
    stop_on_error -
    """

    if worker_queue:
        wq = worker_queue
    else:
        # see if we have a global queue to work with.
        if _wq:
            wq = _wq
        else:
            if num_workers == 0:
                return map(f, seq_args)

            wq = WorkerQueue(num_workers)

    # we short cut it here if the number of workers is 0.
    # normal map should be faster in this case.
    if len(wq.pool) == 0:
        return map(f, seq_args)

    # print("queue size:%s" % wq.queue.qsize())

    # TODO: divide the data (seq_args) into even chunks and
    #       then pass each thread a map(f, equal_part(seq_args))
    #      That way there should be less locking, and overhead.

    results = []
    for sa in seq_args:
        results.append(FuncResult(f))
        wq.do(results[-1], sa)

    # wq.stop()

    if wait:
        # print("wait")
        wq.wait()
        # print("after wait")
        # print("queue size:%s" % wq.queue.qsize())
        if wq.queue.qsize():
            raise RuntimeError("buggy threadmap")
        # if we created a worker queue, we need to stop it.
        if not worker_queue and not _wq:
            # print("stopping")
            wq.stop()
            if wq.queue.qsize():
                um = wq.queue.get()
                if um is not STOP:
                    raise RuntimeError("buggy threadmap")

        # see if there were any errors.  If so raise the first one.  This matches map behaviour.
        # TODO: the traceback doesn't show up nicely.
        # NOTE: TODO: we might want to return the results anyway?  This should be an option.
        if stop_on_error:
            error_ones = list(filter(lambda x: x.exception, results))
            if error_ones:
                raise error_ones[0].exception

        return (x.result for x in results)
    return [wq, results]

