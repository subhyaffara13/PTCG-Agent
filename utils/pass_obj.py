
def pass_obj(f: t.Callable[te.Concatenate[T, P], R]) -> t.Callable[P, R]:
    """Similar to :func:`pass_context`, but only pass the object on the
    context onwards (:attr:`Context.obj`).  This is useful if that object
    represents the state of a nested system.
    """

    def new_func(*args: P.args, **kwargs: P.kwargs) -> R:
        return f(get_current_context().obj, *args, **kwargs)

    return update_wrapper(new_func, f)

