
def spawn_threads_and_init_comms(
    func=None, timeout=TIMEOUT_DEFAULT, world_size=DEFAULT_WORLD_SIZE
):
    """
    Wrapper to use with a test method
    """
    if func is None:
        return partial(
            spawn_threads_and_init_comms, timeout=timeout, world_size=world_size
        )

    def _run_test_method_with_multi_threads(world_size, callback):
        world = _install_threaded_pg()
        global_store = c10d.HashStore()

        def world_is_valid():
            return world == c10d.distributed_c10d._world

        def worker(rank, world_pg, store):
            c10d.init_process_group(
                backend="threaded", rank=rank, world_size=world_size, store=store
            )
            try:
                callback()
            except BaseException as ex:  # noqa: B036
                # Exceptions are handled in MultiThreadedTestCase
                MultiThreadedTestCase.exception_queue.put((rank, sys.exc_info()))
                ProcessLocalGroup.exception_handle(
                    ex
                )  # trigger _terminate event and awaken worker threads
            finally:
                if world_is_valid():
                    c10d.destroy_process_group()

        threads = []
        for rank in range(world_size):
            t = threading.Thread(target=worker, args=(rank, world, global_store))
            t.start()
            threads.append(t)

        return threads

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # TODO: get test name from kwargs
        torch._C._distributed_c10d._set_thread_isolation_mode(True)
        try:
            threads = _run_test_method_with_multi_threads(
                world_size, lambda: func(self, *args, **kwargs)
            )
            # join and error handling
            MultiThreadedTestCase._join_threads(threads, func)
        finally:
            torch._C._distributed_c10d._set_thread_isolation_mode(False)

    return wrapper

