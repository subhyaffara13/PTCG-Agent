
def get_all(store, rank: int, prefix: str, world_size: int):
    r"""
    Given a store and a prefix, the method goes through the array of keys
    of the following format: ``{prefix}{idx}``, where idx is in a range
    from 0 to size, and tries to retrieve the data.

    The Rank0 process waits at the end to make sure all other processes
    finished the procedure before exiting.

    Usage

    ::

     values = get_all(store, "torchelastic/data", 3)
     value1 = values[0]  # retrieves the data for key torchelastic/data0
     value2 = values[1]  # retrieves the data for key torchelastic/data1
     value3 = values[2]  # retrieves the data for key torchelastic/data2

    """
    data_arr = store.multi_get([f"{prefix}{idx}" for idx in range(world_size)])

    barrier_key = _barrier_nonblocking(
        store=store,
        world_size=world_size,
        key_prefix=f"{prefix}/finished",
    )
    if rank == 0:
        # Rank0 runs the TCPStore daemon, as a result it needs to exit last.
        # Otherwise, the barrier may timeout if rank0 process finished the work
        # before other processes finished `get_all` method
        store.wait([barrier_key])

    return data_arr

