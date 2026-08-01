
def is_async_def(t: Type) -> bool:
    """Whether t came from a function defined using `async def`."""
    # In check_func_def(), when we see a function decorated with
    # `@typing.coroutine` or `@async.coroutine`, we change the
    # return type to typing.AwaitableGenerator[...], so that its
    # type is compatible with either Generator or Awaitable.
    # But for the check here we need to know whether the original
    # function (before decoration) was an `async def`.  The
    # AwaitableGenerator type conveniently preserves the original
    # type as its 4th parameter (3rd when using 0-origin indexing
    # :-), so that we can recover that information here.
    # (We really need to see whether the original, undecorated
    # function was an `async def`, which is orthogonal to its
    # decorations.)
    t = get_proper_type(t)
    if (
        isinstance(t, Instance)
        and t.type.fullname == "typing.AwaitableGenerator"
        and len(t.args) >= 4
    ):
        t = get_proper_type(t.args[3])
    return isinstance(t, Instance) and t.type.fullname == "typing.Coroutine"

