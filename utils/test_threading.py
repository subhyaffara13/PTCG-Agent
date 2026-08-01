
def test_threading():
    with m.ostream_redirect(stdout=True, stderr=False):
        # start some threads
        threads = []

        # start some threads
        for _j in range(20):
            threads.append(m.TestThread())

        # give the threads some time to fail
        threads[0].sleep()

        # stop all the threads
        for t in threads:
            t.stop()

        for t in threads:
            t.join()

        # if a thread segfaults, we don't get here
        assert True

