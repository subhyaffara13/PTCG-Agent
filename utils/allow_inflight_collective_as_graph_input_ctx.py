
def allow_inflight_collective_as_graph_input_ctx(value: bool = True):
    """
    Context manager to temporarily set whether inflight collectives are allowed as torch.compile graph inputs.
    Common use case is when the collective is issued in eager (with `async_op=True`) but waited in compiled region:
    ```
    def all_reduce_eager(x):
        y = x * x
        req = dist.all_reduce(y, op=dist.ReduceOp.SUM, async_op=True)
        return y


    @torch.compile(fullgraph=True)
    def all_reduce_wait_compiled(y):
        torch.ops.c10d_functional.wait_tensor(y)
        return y * y


    x = torch.ones(1280, 1280, device="cuda") + self.rank
    # the context manager ensures that `wait_tensor(y)` will wait on the correct work object
    with allow_inflight_collective_as_graph_input_ctx():
        y = all_reduce_eager(x)
        z = all_reduce_wait_compiled(y)
    ```
    With this context manager, when a collective is called, under the hood the work object of the collective
    will be registered in the work registry, and the wait_tensor() in compiled region called on
    the output tensor of the collective will wait on the correct work object.
    """
    previous = torch._C._distributed_c10d._allow_inflight_collective_as_graph_input()

    try:
        torch._C._distributed_c10d._set_allow_inflight_collective_as_graph_input(value)
        yield
    finally:
        torch._C._distributed_c10d._set_allow_inflight_collective_as_graph_input(
            previous
        )

