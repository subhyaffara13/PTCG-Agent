
def _run_in_threads(test_fn, num_threads, parallel):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=test_fn)
        thread.daemon = True
        thread.start()
        if parallel:
            threads.append(thread)
        else:
            thread.join()
    for thread in threads:
        thread.join()

