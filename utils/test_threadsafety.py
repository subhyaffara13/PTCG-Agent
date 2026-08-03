import time

def test_threadsafety():
    def callback(a, caller):
        if a <= 0:
            return 1
        else:
            res = caller(lambda x: callback(x, caller), a - 1)
            return 2*res

    def check(caller):
        caller = CALLERS[caller]

        results = []

        count = 10

        def run():
            time.sleep(0.01)
            r = caller(lambda x: callback(x, caller), count)
            results.append(r)

        threads = [threading.Thread(target=run) for j in range(20)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert_equal(results, [2.0**count]*len(threads))

    for caller in CALLERS.keys():
        check(caller)

