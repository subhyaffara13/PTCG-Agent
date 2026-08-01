
def bool_array_reader(shm_name, n):
    # reader routine for test_read_write_bool_array
    from multiprocessing import shared_memory
    shm = shared_memory.SharedMemory(name=shm_name)
    arr = np.ndarray(n, dtype=np.bool_, buffer=shm.buf)
    for i in range(n):
        while not arr[i]:
            pass

