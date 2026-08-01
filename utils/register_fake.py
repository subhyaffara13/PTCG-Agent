
def register_fake(
    op: _op_identifier,
    func: Callable | None = None,
    /,
    *,
    lib: Library | None = None,
    _stacklevel: int = 1,
    allow_override: bool = False,
):
    r"""Register a FakeTensor implementation ("fake impl") for this operator.

    Also sometimes known as a "meta kernel", "abstract impl".

    An "FakeTensor implementation" specifies the behavior of this operator on
    Tensors that carry no data ("FakeTensor"). Given some input Tensors with
    certain properties (sizes/strides/storage_offset/device), it specifies
    what the properties of the output Tensors are.

    The FakeTensor implementation has the same signature as the operator.
    It is run for both FakeTensors and meta tensors. To write a FakeTensor
    implementation, assume that all Tensor inputs to the operator are
    regular CPU/CUDA/Meta tensors, but they do not have storage, and
    you are trying to return regular CPU/CUDA/Meta tensor(s) as output.
    The FakeTensor implementation must consist of only PyTorch operations
    (and may not directly access the storage or data of any input or
    intermediate Tensors).

    This API may be used as a decorator (see examples).

    For a detailed guide on custom ops, please see
    https://pytorch.org/tutorials/advanced/custom_ops_landing_page.html

    Args:
        op_name: Operator name (along with the overload) or OpOverload object.
        func: Fake tensor implementation.
        lib (Optional[Library]): Library to register the fake tensor to.
        allow_override: Flag controlling if we want to override an
                        existing registered fake impl. This is by default off,
                        and will error you're trying to register a fake impl to
                        an operator that already has a fake impl. This also only
                        applies if the custom operator was not created via
                        torch.library.custom_op, as overriding and existing fake
                        impl is already allowed.

    Examples:
        >>> import torch
        >>> import numpy as np
        >>> from torch import Tensor
        >>>
        >>> # Example 1: an operator without data-dependent output shape
        >>> @torch.library.custom_op("mylib::custom_linear", mutates_args=())
        >>> def custom_linear(x: Tensor, weight: Tensor, bias: Tensor) -> Tensor:
        >>>     raise NotImplementedError("Implementation goes here")
        >>>
        >>> @torch.library.register_fake("mylib::custom_linear")
        >>> def _(x, weight, bias):
        >>>     assert x.dim() == 2
        >>>     assert weight.dim() == 2
        >>>     assert bias.dim() == 1
        >>>     assert x.shape[1] == weight.shape[1]
        >>>     assert weight.shape[0] == bias.shape[0]
        >>>     assert x.device == weight.device
        >>>
        >>>     return (x @ weight.t()) + bias
        >>>
        >>> with torch._subclasses.fake_tensor.FakeTensorMode():
        >>>     x = torch.randn(2, 3)
        >>>     w = torch.randn(3, 3)
        >>>     b = torch.randn(3)
        >>>     y = torch.ops.mylib.custom_linear(x, w, b)
        >>>
        >>> assert y.shape == (2, 3)
        >>>
        >>> # Example 2: an operator with data-dependent output shape
        >>> @torch.library.custom_op("mylib::custom_nonzero", mutates_args=())
        >>> def custom_nonzero(x: Tensor) -> Tensor:
        >>>     x_np = x.numpy(force=True)
        >>>     res = np.stack(np.nonzero(x_np), axis=1)
        >>>     return torch.tensor(res, device=x.device)
        >>>
        >>> @torch.library.register_fake("mylib::custom_nonzero")
        >>> def _(x):
        >>> # Number of nonzero-elements is data-dependent.
        >>> # Since we cannot peek at the data in an fake impl,
        >>> # we use the ctx object to construct a new symint that
        >>> # represents the data-dependent size.
        >>>     ctx = torch.library.get_ctx()
        >>>     nnz = ctx.new_dynamic_size()
        >>>     shape = [nnz, x.dim()]
        >>>     result = x.new_empty(shape, dtype=torch.int64)
        >>>     return result
        >>>
        >>> from torch.fx.experimental.proxy_tensor import make_fx
        >>>
        >>> x = torch.tensor([0, 1, 2, 3, 4, 0])
        >>> trace = make_fx(torch.ops.mylib.custom_nonzero, tracing_mode="symbolic")(x)
        >>> trace.print_readable()
        >>>
        >>> assert torch.allclose(trace(x), torch.ops.mylib.custom_nonzero(x))

    """
    if not isinstance(
        op, (str, torch._ops.OpOverload, torch._library.custom_ops.CustomOpDef)
    ):
        raise ValueError(f"register_fake({op}): got unexpected type for op: {type(op)}")
    if isinstance(op, torch._ops.OpOverload):
        op = op._name
    opdef = _maybe_get_opdef(op)
    if opdef is not None:
        if func is None:
            return opdef.register_fake
        else:
            return opdef.register_fake(func)
    if not isinstance(op, str):
        raise AssertionError(f"op must be str at this point, got {type(op).__name__}")

    stacklevel = _stacklevel

    def register(func):
        namespace, op_name = torch._library.utils.parse_namespace(op)
        if lib is None:
            use_lib = Library(namespace, "FRAGMENT")
            _keep_alive.append(use_lib)
        else:
            use_lib = lib
        use_lib._register_fake(
            op_name, func, _stacklevel=stacklevel + 1, allow_override=allow_override
        )
        return func

    if func is None:
        return register
    else:
        stacklevel += 1
        return register(func)


def register_fake(hop, fn: None = None) -> Callable[[F], F]: ...


def register_fake(hop, fn: F) -> F: ...


def register_fake(hop, fn=None):
    """
    Register a fake function for a HOP. This is conceptually equivalent of the
    register_fake utility for the custom ops. The registered function is called
    inside the fake_tensor _dispatch_impl.
    """
    if hop in registered_hop_fake_fns:
        raise AssertionError(f"hop {hop} already registered in registered_hop_fake_fns")

    def register(func: F) -> F:
        from torch._subclasses.fake_tensor import FakeTensorMode

        redirect_to_mode(hop, FakeTensorMode)

        registered_hop_fake_fns[hop] = func
        return func

    if fn is None:
        return register
    return register(fn)

