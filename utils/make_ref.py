
def make_ref(obj: T, callback: c.Callable[[ref[T]], None] | None = None) -> ref[T]:
    if inspect.ismethod(obj):
        return WeakMethod(obj, callback)  # type: ignore[arg-type, return-value]

    return ref(obj, callback)

