
def remote_add(t1, t2, dst: str):  # noqa: E999
    return rpc_async(dst, local_add, (t1, t2)).wait()

