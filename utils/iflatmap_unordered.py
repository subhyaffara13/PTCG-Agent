from typing import Callable

def iflatmap_unordered(
    pool: multiprocessing.pool.ThreadPool,
    func: Callable[..., Iterable[T]],
    *,
    kwargs_list: list[dict],
) -> Iterable[T]:
    """
    Takes a function that returns an iterable of items, and run it in parallel using threads to return the flattened iterable of items as they arrive.

    This is inspired by those three `map()` variants, and is the mix of all three:

    * `imap()`: like `map()` but returns an iterable instead of a list of results
    * `imap_unordered()`: like `imap()` but the output is sorted by time of arrival
    * `flatmap()`: like `map()` but given a function which returns a list, `flatmap()` returns the flattened list that is the concatenation of all the output lists
    """
    queue: Queue[T] = Queue()
    async_results = [pool.apply_async(_write_generator_to_queue, (queue, func, kwargs)) for kwargs in kwargs_list]
    try:
        while True:
            try:
                yield queue.get(timeout=0.05)
            except Empty:
                if all(async_result.ready() for async_result in async_results) and queue.empty():
                    break
    except KeyboardInterrupt:
        pass
    finally:
        # we get the result in case there's an error to raise
        try:
            [async_result.get(timeout=0.05) for async_result in async_results]
        except multiprocessing.TimeoutError:
            pass

