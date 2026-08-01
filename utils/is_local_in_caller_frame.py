
def is_local_in_caller_frame(obj):
    """
    Helper function used in detecting chained assignment.

    If the pandas object (DataFrame/Series) is a local variable
    in the caller's frame, it should not be a case of chained
    assignment or method call.

    For example:

    def test():
        df = pd.DataFrame(...)
        df["a"] = 1  # not chained assignment

    Inside ``df.__setitem__``, we call this function to check whether `df`
    (`self`) is a local variable in `test` frame (the frame calling setitem). If
    so, we know it is not a case of chained assignment (even when the refcount
    of `df` is below the threshold due to optimization of local variables).
    """
    frame = sys._getframe(2)
    for v in frame.f_locals.values():
        if v is obj:
            return True
    return False

