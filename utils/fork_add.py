
def fork_add(t1, t2, dst: str):
    fut = torch.jit._fork(remote_add, t1, t2, dst)
    return torch.jit._wait(fut)

