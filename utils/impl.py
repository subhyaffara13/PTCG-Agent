
def impl(
    qualname: str,
    types: str | Sequence[str],
    func: None = None,
    *,
    lib: Library | None = None,
) -> Callable[[Callable[..., object]], None]: ...


def impl(
    qualname: str,
    types: str | Sequence[str],
    func: Callable[..., object],
    *,
    lib: Library | None = None,
) -> None: ...


def impl(
    lib: Library,
    name: str,
    dispatch_key: str = "",
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]: ...


def impl(
    qualname: str,
    types: str | Sequence[str],
    func: Callable[_P, _T] | None = None,
    *,
    lib: Library | None = None,
) -> object:
    """Register an implementation for a device type for this operator.

    You may pass "default" for ``types`` to register this implementation as the
    default implementation for ALL device types.
    Please only use this if the implementation truly supports all device types;
    for example, this is true if it is a composition of built-in PyTorch operators.

    This API may be used as a decorator. You can use nested decorators
    with this API provided they return a function and are placed inside
    this API (see Example 2).

    Some valid types are: "cpu", "cuda", "xla", "mps", "ipu", "xpu".

    Args:
        qualname (str): Should be a string that looks like "namespace::operator_name".
        types (str | Sequence[str]): The device types to register an impl to.
        lib (Optional[Library]): If provided, the lifetime of this registration
            will be tied to the lifetime of the Library object.

    Examples:
        >>> # xdoctest: +SKIP("Requires Python <= 3.11")
        >>> import torch
        >>> import numpy as np
        >>> # Example 1: Register function.
        >>> # Define the operator
        >>> torch.library.define("mylib::mysin", "(Tensor x) -> Tensor")
        >>>
        >>> # Add implementations for the cpu device
        >>> @torch.library.impl("mylib::mysin", "cpu")
        >>> def f(x):
        >>>     return torch.from_numpy(np.sin(x.numpy()))
        >>>
        >>> x = torch.randn(3)
        >>> y = torch.ops.mylib.mysin(x)
        >>> assert torch.allclose(y, x.sin())
        >>>
        >>> # Example 2: Register function with decorator.
        >>> def custom_decorator(func):
        >>>     def wrapper(*args, **kwargs):
        >>>         return func(*args, **kwargs) + 1
        >>>     return wrapper
        >>>
        >>> # Define the operator
        >>> torch.library.define("mylib::sin_plus_one", "(Tensor x) -> Tensor")
        >>>
        >>> # Add implementations for the operator
        >>> @torch.library.impl("mylib::sin_plus_one", "cpu")
        >>> @custom_decorator
        >>> def f(x):
        >>>     return torch.from_numpy(np.sin(x.numpy()))
        >>>
        >>> # Call the new operator from torch.ops.
        >>> x = torch.randn(3)
        >>>
        >>> y1 = torch.ops.mylib.sin_plus_one(x)
        >>> y2 = torch.sin(x) + 1
        >>> assert torch.allclose(y1, y2)
    """

    return _impl(qualname, types, func, lib=lib, disable_dynamo=False)


def impl(qualname, *, device_types=("cpu", "cuda"), func=None):
    r"""Register an implementation for a device type for this custom op.

    If the op is passed multiple Tensor inputs with different device
    types, it will dispatch to the registered implementation for the highest
    priority device type among those present.
    The supported device types, in order of priority, are {'cuda', 'cpu'}.

    This API may be used as a decorator (see examples).

    For a detailed guide on custom ops, please see
    https://docs.google.com/document/d/1aGWtgxV3HppuxQAdddyPrs74_aEntpkYt9MalnCKnhk

    Arguments:
        device_types (str or Iterable[str]): the device type(s) to register the function for.

    Example::

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CUDA)
        >>> import torch
        >>> import numpy as np
        >>> from torch import Tensor
        >>>
        >>> # Step 1: define the custom op.
        >>> # We need to provide the API a "prototype function"
        >>> # (a function that returns NotImplementedError), from which
        >>> # we will infer the types of the inputs and outputs.
        >>> @torch._custom_ops.custom_op("mylibrary::numpy_cos")
        >>> def numpy_cos(x: Tensor) -> Tensor:
        >>>     raise NotImplementedError
        >>>
        >>> # The custom op is now accessible via the torch.ops module:
        >>> torch.ops.mylibrary.numpy_cos
        >>>
        >>> # Step 2: Register an implementation for various PyTorch subsystems
        >>>
        >>> # Register an implementation for CPU tensors
        >>> @torch._custom_ops.impl("mylibrary::numpy_cos", device_types="cpu")
        >>> def numpy_cos_impl_cpu(x):
        >>>     return torch.from_numpy(np.cos(x.numpy()))
        >>>
        >>> # Register an implementation for CUDA tensors
        >>> @torch._custom_ops.impl("mylibrary::numpy_cos", device_types="cuda")
        >>> def numpy_cos_impl_cuda(x):
        >>>     return torch.from_numpy(np.cos(x.cpu().numpy())).to(x.device)
        >>>
        >>> x = torch.randn(3)
        >>> torch.ops.mylibrary.numpy_cos(x)  # calls numpy_cos_impl_cpu
        >>>
        >>> x_cuda = x.cuda()
        >>> torch.ops.mylibrary.numpy_cos(x)  # calls numpy_cos_impl_cuda

    """

    def inner(func):
        custom_op = _find_custom_op(qualname, also_check_torch_library=True)
        custom_op.impl(device_types, _stacklevel=3)(func)
        return func

    if func is None:
        return inner
    return inner(func)


def impl(
    func: _OpTypes | pytree.TreeSpec,
    in_spec: pytree.TreeSpec,
    flat_args: tuple[Unpack[_Ts]],
    checked_output: bool,
) -> _FXOutput:
    if isinstance(func, pytree.TreeSpec):
        # assume _ConstantFunction
        func = pytree._retrieve_constant(func)
        if not isinstance(func, _ConstantFunction):
            raise AssertionError(
                f"expected retrieved constant to be _ConstantFunction, got {type(func)}"
            )

    from torch._higher_order_ops.invoke_leaf_function import unflatten_args_with_modules

    with unflatten_args_with_modules(flat_args, in_spec) as (args, kwargs):
        out = func(*args, **kwargs)

    if checked_output:
        # For "normal" usage all outputs must either be graphable or
        # lists/tuples of graphables.
        if not is_valid_output(out):
            raise AssertionError(
                f"output must be graphable or nested list/tuple of graphables, got {type(out)}"
            )
    return out

