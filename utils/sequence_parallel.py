
def sequence_parallel(fs):
    with ThreadPool(len(fs)) as pool:
        return pool.map(lambda f: f(), fs)

