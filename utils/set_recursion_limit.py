
def set_recursion_limit(limit: int) -> None:
    """
    Sets an internal dynamo recursion limit. The limit must be >= 1, or -1 to reset
    to the default (unset) state.

    This is possibly needed in Python 3.12-3.13 since there is a separate C recursion limit
    that is not visible at the Python level. If you are getting RecursionErrors during
    Dynamo compilation and `sys.setrecursionlimit()` doesn't help, this function may alleviate
    the issue.

    NOTE: this function does NOT call `sys.setrecursionlimit()` - the user is expected to manually
        call this if required. This is because the 2 recursion limits are not sync'd up - e.g. in
        Python 3.12, functions can be inline-evaluated, which apparently doesn't use up the C stack.

    WARNING: increasing the recursion limit to an arbitrary large value may cause segfaults
        due to stack overflows! You can try also try to manually increase the stack size, e.g.
        with `$ ulimit -s ...`
    """
    torch._C._dynamo.eval_frame.set_c_recursion_limit(limit)


def SetRecursionLimit(new_limit):
  global _recursion_limit
  _recursion_limit = new_limit

