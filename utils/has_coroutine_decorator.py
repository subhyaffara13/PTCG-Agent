
def has_coroutine_decorator(t: Type) -> bool:
    """Whether t came from a function decorated with `@coroutine`."""
    t = get_proper_type(t)
    return isinstance(t, Instance) and t.type.fullname == "typing.AwaitableGenerator"

