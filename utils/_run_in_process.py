
def _run_in_process(target, *args, **kwargs):
    test_fn = target if len(args) == 0 else args[0]
    # Do not need to wait much, 10s should be more than enough.
    timeout = 0.1 if test_fn is _intentional_deadlock else 10
    process = multiprocessing.Process(target=target, args=args, kwargs=kwargs)
    process.daemon = True
    try:
        t_start = time.time()
        process.start()
        if timeout >= 100:  # For debugging.
            print(
                "\nprocess.pid STARTED", process.pid, (sys.argv, target, args, kwargs)
            )
            print(f"COPY-PASTE-THIS: gdb {sys.argv[0]} -p {process.pid}", flush=True)
        process.join(timeout=timeout)
        if timeout >= 100:
            print("\nprocess.pid JOINED", process.pid, flush=True)
        t_delta = time.time() - t_start
        if process.exitcode == 66 and m.defined_THREAD_SANITIZER:  # Issue #2754
            # WOULD-BE-NICE-TO-HAVE: Check that the message below is actually in the output.
            # Maybe this could work:
            # https://gist.github.com/alexeygrigorev/01ce847f2e721b513b42ea4a6c96905e
            pytest.skip(
                "ThreadSanitizer: starting new threads after multi-threaded fork is not supported."
            )
        elif test_fn is _intentional_deadlock:
            assert process.exitcode is None
            return 0

        if process.exitcode is None:
            assert t_delta > 0.9 * timeout
            msg = "DEADLOCK, most likely, exactly what this test is meant to detect."
            if env.PYPY and env.WIN:
                pytest.skip(msg)
            raise RuntimeError(msg)
        return process.exitcode
    finally:
        if process.is_alive():
            process.terminate()

