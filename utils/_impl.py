
def _impl(
    qualname: str,
    types: str | Sequence[str],
    func: None = None,
    *,
    lib: Library | None = None,
    disable_dynamo: bool = False,
) -> Callable[[Callable[..., object]], None]: ...


def _impl(
    qualname: str,
    types: str | Sequence[str],
    func: Callable[..., object],
    *,
    lib: Library | None = None,
    disable_dynamo: bool = False,
) -> None: ...


def _impl(
    qualname: str,
    types: str | Sequence[str],
    func: Callable[..., object] | None = None,
    *,
    lib: Library | None = None,
    disable_dynamo: bool = False,
) -> Callable[[Callable[..., object]], None] | None:
    # See impl()
    if isinstance(types, str):
        types = (types,)
    keys = set({})
    for typ in types:
        is_dispatch_key = torch._C._parse_dispatch_key(typ)
        if is_dispatch_key:
            # We also support passing a DispatchKey to impl. Please prefer using
            # the higher-level torch.library APIs and only pass DispatchKey to
            # torch.library.impl with caution (or even better, don't use this
            # option and file an issue on GitHub for what you need).
            # We don't advertise this to users because
            # it is very easy to shoot yourself in the foot.
            keys.add(typ)
        else:
            keys.add(_device_type_to_key(typ))

    def register_(func: Callable[..., object]) -> None:
        namespace, _ = torch._library.utils.parse_namespace(qualname)

        if lib is None:
            use_lib = Library(namespace, "FRAGMENT")
            _keep_alive.append(use_lib)
        else:
            use_lib = lib
        if disable_dynamo:

            @torch._disable_dynamo
            def func_no_dynamo(*args, **kwargs):
                return func(*args, **kwargs)

            for key in keys:
                use_lib.impl(qualname, func_no_dynamo, key)
        else:
            for key in keys:
                use_lib.impl(qualname, func, key)

    if func is None:
        return register_
    else:
        register_(func)
        return None

