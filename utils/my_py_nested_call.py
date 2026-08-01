
def my_py_nested_call(t1, t2, dst, world_size, hops):
    next_dst = (dst + 1) % world_size
    if hops > 0:
        return rpc.rpc_sync(
            worker_name(next_dst),
            my_py_nested_call,
            args=(t1, t2, next_dst, world_size, hops - 1),
        )
    else:
        return rpc.rpc_sync(worker_name(next_dst), my_py_add, args=(t1, t2))

