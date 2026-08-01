
def bool_array_writer(shm_name, n):
    # writer routine for test_read_write_bool_array
    import time
    from multiprocessing import shared_memory
    shm = shared_memory.SharedMemory(name=shm_name)
    arr = np.ndarray(n, dtype=np.bool_, buffer=shm.buf)
    for i in range(n):
        arr[i] = True
        time.sleep(0.00001)

