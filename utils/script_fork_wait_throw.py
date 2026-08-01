
def script_fork_wait_throw(invalue):
    fut = torch.jit._fork(script_raise_func, invalue)
    value = torch.jit._wait(fut)
    return value

