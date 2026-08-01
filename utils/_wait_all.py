
def _wait_all():
    r"""
    A context manager that collects all futures returned by ``rpc_async`` and
    waits them on the context manager's exit; relieving the user of needing
    to explicitly call wait.


    Example::
        >>> # xdoctest: +SKIP("distributed")
        >>> # On worker 0:
        >>> import torch
        >>> import torch.distributed.rpc as rpc
        >>> rpc.init_rpc("worker0", rank=0, world_size=2)
        >>> with rpc._wait_all():
        >>>    fut_1 = rpc.rpc_async(dst, torch.add, (torch.ones(2, 2), 1))
        >>>    fut_2 = rpc.rpc_async(dst, torch.add, (torch.ones(2, 2), 1))
        >>> #fut_1 and fut_2 are waited on
    """
    _thread_local_var.future_list = []
    try:
        yield
    finally:
        try:
            torch.futures.wait_all(_thread_local_var.future_list)
        finally:
            del _thread_local_var.future_list

