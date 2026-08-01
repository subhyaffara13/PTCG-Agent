
def test_read_write_bool_array():
    # See: gh-30389
    #
    # Prior to Python 3.13, boolean scalar singletons (np.True / np.False) were
    # regular reference-counted objects. Due to the double evaluation in
    # PyArrayScalar_RETURN_BOOL_FROM_LONG, concurrent reads and writes of a
    # boolean array could corrupt their refcounts, potentially causing a crash
    # (e.g., `free(): invalid pointer`).
    #
    # This test creates a multi-process race between a writer and a reader to
    # ensure that NumPy does not exhibit such failures.
    from concurrent.futures import ProcessPoolExecutor
    from multiprocessing import shared_memory
    n = 10000
    shm = shared_memory.SharedMemory(create=True, size=n)
    ctx = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=2, mp_context=ctx) as executor:
        f_writer = executor.submit(bool_array_writer, shm.name, n)
        f_reader = executor.submit(bool_array_reader, shm.name, n)
    shm.unlink()
    f_writer.result()
    f_reader.result()

