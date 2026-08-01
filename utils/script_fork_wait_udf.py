
def script_fork_wait_udf(tensor):
    fut = torch.jit._fork(script_add_ones, tensor)
    x = torch.jit._wait(fut)
    return x

