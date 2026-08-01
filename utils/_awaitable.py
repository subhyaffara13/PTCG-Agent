
def _awaitable(func, *args, **kwargs):
    r"""Create Await object that will call specified functioni with specified args, when it is requested for the result."""
    return torch._C._awaitable(func, *args, **kwargs)

