
def mirror_sync_methods(obj):
    """Populate sync and async methods for obj

    For each method will create a sync version if the name refers to an async method
    (coroutine) and there is no override in the child class; will create an async
    method for the corresponding sync method if there is no implementation.

    Uses the methods specified in
    - async_methods: the set that an implementation is expected to provide
    - default_async_methods: that can be derived from their sync version in
      AbstractFileSystem
    - AsyncFileSystem: async-specific default coroutines
    """
    from fsspec import AbstractFileSystem

    for method in set(async_methods + dir(AsyncFileSystem)):
        if not method.startswith("_"):
            continue
        smethod = method[1:]
        if private.match(method):
            isco = inspect.iscoroutinefunction(getattr(obj, method, None))
            unsync = getattr(getattr(obj, smethod, False), "__func__", None)
            is_default = unsync is getattr(AbstractFileSystem, smethod, "")
            if isco and is_default:
                mth = sync_wrapper(getattr(obj, method), obj=obj)
            elif inspect.isasyncgenfunction(getattr(obj, method, None)) and is_default:
                mth = async_gen_wrapper(getattr(obj, method), obj=obj)
            else:
                continue
            setattr(obj, smethod, mth)
            if not mth.__doc__:
                mth.__doc__ = getattr(
                    getattr(AbstractFileSystem, smethod, None), "__doc__", ""
                )

