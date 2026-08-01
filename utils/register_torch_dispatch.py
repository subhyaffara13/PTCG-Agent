
def register_torch_dispatch(
    op: _op_identifier,
    torch_dispatch_class: Any,
    func: Callable | None = None,
    /,
    *,
    lib: Library | None = None,
):
    r"""Registers a torch_dispatch rule for the given operator and ``torch_dispatch_class``.

    This allows for open registration to specify the behavior between the operator
    and the ``torch_dispatch_class`` without needing to modify the ``torch_dispatch_class``
    or the operator directly.

    The ``torch_dispatch_class`` is either a Tensor subclass with ``__torch_dispatch__`` or a
    TorchDispatchMode.

    If it is a Tensor subclass, we expect ``func`` to have the following signature:
    ``(cls, func: OpOverload, types: Tuple[type, ...], args, kwargs) -> Any``

    If it is a TorchDispatchMode, we expect ``func`` to have the following signature:
    ``(mode, func: OpOverload, types: Tuple[type, ...], args, kwargs) -> Any``

    ``args`` and ``kwargs`` will have been normalized the same way they are
    in ``__torch_dispatch__`` (see :ref:`torch-dispatch-calling-convention`).

    Examples:

        >>> import torch
        >>>
        >>> @torch.library.custom_op("mylib::foo", mutates_args={})
        >>> def foo(x: torch.Tensor) -> torch.Tensor:
        >>>     return x.clone()
        >>>
        >>> class MyMode(torch.utils._python_dispatch.TorchDispatchMode):
        >>>     def __torch_dispatch__(self, func, types, args=(), kwargs=None):
        >>>         return func(*args, **kwargs)
        >>>
        >>> @torch.library.register_torch_dispatch("mylib::foo", MyMode)
        >>> def _(mode, func, types, args, kwargs):
        >>>     x, = args
        >>>     return x + 1
        >>>
        >>> x = torch.randn(3)
        >>> y = foo(x)
        >>> assert torch.allclose(y, x)
        >>>
        >>> with MyMode():
        >>>     y = foo(x)
        >>> assert torch.allclose(y, x + 1)

    """
    if not isinstance(
        op, (str, torch._ops.OpOverload, torch._library.custom_ops.CustomOpDef)
    ):
        raise ValueError(
            f"register_torch_dispatch({op}): got unexpected type for op: {type(op)}"
        )
    if isinstance(op, torch._ops.OpOverload):
        op = op._name
    opdef = _maybe_get_opdef(op)
    if opdef is not None:
        return opdef.register_torch_dispatch(torch_dispatch_class, func)
    if not isinstance(op, str):
        raise AssertionError(f"op must be str at this point, got {type(op).__name__}")

    def register(func):
        namespace, op_name = torch._library.utils.parse_namespace(op)
        if lib is None:
            use_lib = Library(namespace, "FRAGMENT")
            _keep_alive.append(use_lib)
        else:
            use_lib = lib
        use_lib._register_torch_dispatch_rule(op_name, torch_dispatch_class, func)
        return func

    if func is None:
        return register
    else:
        return register(func)

