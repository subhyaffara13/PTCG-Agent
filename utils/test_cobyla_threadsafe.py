
def test_cobyla_threadsafe():

    # Verify that cobyla is threadsafe. Will segfault if it is not.

    import concurrent.futures
    import time

    def objective1(x):
        time.sleep(0.1)
        return x[0]**2

    def objective2(x):
        time.sleep(0.1)
        return (x[0]-1)**2

    min_method = "COBYLA"

    def minimizer1():
        return optimize.minimize(objective1,
                                      [0.0],
                                      method=min_method)

    def minimizer2():
        return optimize.minimize(objective2,
                                      [0.0],
                                      method=min_method)

    with concurrent.futures.ThreadPoolExecutor() as pool:
        tasks = []
        tasks.append(pool.submit(minimizer1))
        tasks.append(pool.submit(minimizer2))
        for t in tasks:
            t.result()

