
def get_recursion_limit() -> int:
    """
    Returns the internal dynamo recursion limit set by `torch._dynamo.set_recursion_limit`.

    Returns -1 if no c recursion limit has been set.
    """
    return torch._C._dynamo.eval_frame.get_c_recursion_limit()

