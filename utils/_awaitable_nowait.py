
def _awaitable_nowait(o):
    r"""Create completed Await with specified result."""
    return torch._C._awaitable_nowait(o)

