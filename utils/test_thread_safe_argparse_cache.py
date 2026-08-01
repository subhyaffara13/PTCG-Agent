
def test_thread_safe_argparse_cache():
    b = threading.Barrier(8)

    def call_thread_func():
        b.wait()
        thread_func(arg1=3, arg2=None)

    tasks = [threading.Thread(target=call_thread_func) for _ in range(8)]
    [t.start() for t in tasks]
    [t.join() for t in tasks]

