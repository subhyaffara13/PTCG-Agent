
def _awaitable_wait(aw):
    r"""Request await the result of execution, if Await is not completed yet, the func will be called immediately."""
    return torch._C._awaitable_wait(aw)

