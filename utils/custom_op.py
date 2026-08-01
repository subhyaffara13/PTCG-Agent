
def custom_op(qualname, func_or_schema=None):
    r"""Register a new custom operator

    In PyTorch, defining an op (short for "operator") is a two step-process:
    - we need to define the op (by providing an operator name and schema)
    - we need to implement behavior for how the operator interacts with
      various PyTorch subsystems, like CPU/CUDA Tensors, Autograd, etc.

    This entrypoint defines the custom operator (the first step)
    you must then perform the second step by calling various
    ``impl_*`` APIs.

    This API may be used as a decorator (see examples).

    For a detailed guide on custom ops, please see
    https://docs.google.com/document/d/1aGWtgxV3HppuxQAdddyPrs74_aEntpkYt9MalnCKnhk

    Arguments:
        qualname (str): Should be a string that looks like
            "namespace::operator_name". Operators in PyTorch need a namespace to
            avoid name collisions; a given operator may only be created once.
            If you are writing a Python library, we recommend the namespace to
            be the name of your top-level module.
        func_or_schema (Union[Callable, str]): Each PyTorch operator needs a
            schema that tells PyTorch the types of the inputs/outputs.
            If this is a Callable, we will automatically infer the schema from
            the type annotations on the function (see examples). Otherwise,
            if you don't want to use type annotations, you may provide us the
            schema string.

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
        >>> @torch._custom_ops.custom_op("mylibrary::numpy_sin")
        >>> def numpy_sin(x: Tensor) -> Tensor:
        >>>     raise NotImplementedError
        >>>
        >>> # The custom op is now accessible via the torch.ops module:
        >>> torch.ops.mylibrary.numpy_sin
        >>>
        >>> # Step 2: Register an implementation for various PyTorch subsystems
        >>>
        >>> # Register an implementation for CPU tensors
        >>> @torch._custom_ops.impl("mylibrary::numpy_sin", device_types="cpu")
        >>> def numpy_sin_impl_cpu(x):
        >>>     return torch.from_numpy(np.sin(x.numpy()))
        >>>
        >>> # Register an implementation for CUDA tensors
        >>> @torch._custom_ops.impl("mylibrary::numpy_sin", device_types="cuda")
        >>> def numpy_sin_impl_cuda(x):
        >>>     return torch.from_numpy(np.sin(x.cpu().numpy())).to(x.device)
        >>>
        >>> x = torch.randn(3)
        >>> torch.ops.mylibrary.numpy_sin(x)  # calls numpy_sin_impl_cpu
        >>>
        >>> x_cuda = x.cuda()
        >>> torch.ops.mylibrary.numpy_sin(x)  # calls numpy_sin_impl_cuda

    """
    ns, name = parse_qualname(qualname)
    validate_namespace(ns)

    def inner(func):
        if not inspect.isfunction(func):
            raise ValueError(
                f"custom_op(...)(func): Expected `func` to be a Python "
                f"function, got: {type(func)}"
            )

        if func.__name__ != name:
            raise ValueError(
                f"custom_op(qualname='{qualname}', ...)(func): expected `func` "
                f"to have name '{name}' but got '{func.__name__}'. "
                f"Please either change the name of `func` or the qualname that "
                f"is passed to `custom_op`"
            )

        schema = infer_schema(func, mutates_args=())
        _custom_op_with_schema(qualname, schema)
        return func

    if func_or_schema is None:
        return inner
    if isinstance(func_or_schema, str):
        _custom_op_with_schema(qualname, func_or_schema)
    else:
        return inner(func_or_schema)


def custom_op(qualname: str, manual_schema: str | None = None) -> typing.Callable:
    r"""
    This API is deprecated, please use torch.library.custom_op instead
    """
    warn_deprecated()

    def inner(func):
        if not inspect.isfunction(func):
            raise ValueError(
                f"custom_op(...)(func): Expected `func` to be a Python "
                f"function, got: {type(func)}"
            )

        ns, name = parse_qualname(qualname)
        validate_namespace(ns)
        if func.__name__ != name:
            raise ValueError(
                f"custom_op(qualname='{qualname}', ...)(func): expected `func` "
                f"to have name '{name}' but got '{func.__name__}'. "
                f"Please either change the name of `func` or the qualname that "
                f"is passed to `custom_op`"
            )

        schema = (
            infer_schema(func, mutates_args=())
            if manual_schema is None
            else manual_schema
        )
        schema_str = f"{name}{schema}"
        function_schema = FunctionSchema.parse(schema_str)
        validate_schema(function_schema)
        if manual_schema is not None:
            validate_function_matches_schema(function_schema, func)

        lib = library.Library(ns, "FRAGMENT")
        lib.define(schema_str)
        ophandle = find_ophandle_or_throw(ns, function_schema.name)
        result = CustomOp(
            lib, ns, function_schema, name, ophandle, _private_access=True
        )

        result.__name__ = func.__name__  # pyrefly: ignore [bad-assignment]
        result.__module__ = func.__module__
        result.__doc__ = func.__doc__

        library.impl(lib, result._opname, "Autograd")(
            autograd_kernel_indirection(weakref.proxy(result))
        )

        torch._C._dispatch_set_report_error_callback(
            ophandle, functools.partial(report_error_callback, weakref.proxy(result))
        )

        return result

    return inner


def custom_op(
    name: str,
    fn: None = None,
    /,
    *,
    mutates_args: str | Iterable[str],
    device_types: device_types_t = None,
    schema: str | None = None,
    tags: Sequence[_C.Tag] | None = None,
) -> Callable[[Callable[..., object]], "CustomOpDef"]: ...


def custom_op(
    name: str,
    fn: Callable[..., object],
    /,
    *,
    mutates_args: str | Iterable[str],
    device_types: device_types_t = None,
    schema: str | None = None,
    tags: Sequence[_C.Tag] | None = None,
) -> "CustomOpDef": ...


def custom_op(
    name: str,
    fn: Callable | None = None,
    /,
    *,
    mutates_args: str | Iterable[str],
    device_types: device_types_t = None,
    schema: str | None = None,
    tags: Sequence[_C.Tag] | None = None,
) -> Union[Callable[[Callable[..., object]], "CustomOpDef"], "CustomOpDef"]:
    """Wraps a function into custom operator.

    Reasons why you may want to create a custom op include:
    - Wrapping a third-party library or custom kernel to work with PyTorch
    subsystems like Autograd.
    - Preventing torch.compile/export/FX tracing from peeking inside your function.

    This API is used as a decorator around a function (please see examples).
    The provided function must have type hints; these are needed to interface
    with PyTorch's various subsystems.

    Args:
        name (str): A name for the custom op that looks like "{namespace}::{name}",
            e.g. "mylib::my_linear". The name is used as the op's stable identifier
            in PyTorch subsystems (e.g. torch.export, FX graphs).
            To avoid name collisions, please use your project name as the namespace;
            e.g. all custom ops in pytorch/fbgemm use "fbgemm" as the namespace.
        mutates_args (Iterable[str] or "unknown"): The names of args that the function mutates.
            This MUST be accurate, otherwise, the behavior is undefined. If "unknown",
            it pessimistically assumes that all inputs to the operator are being mutated.
        device_types (str | None | Sequence[str]): The device type(s) the function
            is valid for. If no device type is provided, then the function
            is used as the default implementation for all device types.
            Examples: "cpu", "cuda".
            When registering a device-specific implementation for an operator that accepts no Tensors,
            we require the operator to have a "device: torch.device argument".
        schema (str | None): A schema string for the operator. If None
            (recommended) we'll infer a schema for the operator from its type
            annotations. We recommend letting us infer a schema unless you
            have a specific reason not to.
            Example: "(Tensor x, int y) -> (Tensor, Tensor)".

    The following types are supported for the wrapped function's input parameters:

        - Scalars: ``int``, ``float``, ``bool``, ``str``, ``torch.types.Number``
        - Tensors: ``torch.Tensor``
        - Enums/devices: ``torch.dtype``, ``torch.device``
        - Flat list of the same type: ``list[torch.Tensor]``,
          ``list[int]``, ``list[float]``, ``list[bool]``,
          ``list[torch.types.Number]``
        - Optionals: ``Optional`` of any of the above scalar/tensor types
        - Types registered via :func:`torch.library.register_opaque_type`

    The following types are supported for the return value:

        ``torch.Tensor``, ``list[torch.Tensor]``, ``int``, ``float``,
        ``bool``, ``torch.types.Number``.

    .. note::
        We recommend not passing in a ``schema`` arg and instead letting us infer
        it from the type annotations. It is error-prone to write your own schema.
        You may wish to provide your own schema if our interpretation of
        the type annotation is not what you want.
        For more info on how to write a schema string, see
        `here <https://github.com/pytorch/pytorch/blob/main/aten/src/ATen/native/README.md#func>`_

    Examples::
        >>> import torch
        >>> from torch import Tensor
        >>> from torch.library import custom_op
        >>> import numpy as np
        >>>
        >>> @custom_op("mylib::numpy_sin", mutates_args=())
        >>> def numpy_sin(x: Tensor) -> Tensor:
        >>>     x_np = x.cpu().numpy()
        >>>     y_np = np.sin(x_np)
        >>>     return torch.from_numpy(y_np).to(device=x.device)
        >>>
        >>> x = torch.randn(3)
        >>> y = numpy_sin(x)
        >>> assert torch.allclose(y, x.sin())
        >>>
        >>> # Example of a custom op that only works for one device type.
        >>> @custom_op("mylib::numpy_sin_cpu", mutates_args=(), device_types="cpu")
        >>> def numpy_sin_cpu(x: Tensor) -> Tensor:
        >>>     x_np = x.numpy()
        >>>     y_np = np.sin(x_np)
        >>>     return torch.from_numpy(y_np)
        >>>
        >>> x = torch.randn(3)
        >>> y = numpy_sin_cpu(x)
        >>> assert torch.allclose(y, x.sin())
        >>>
        >>> # Example of a custom op that mutates an input
        >>> @custom_op("mylib::numpy_sin_inplace", mutates_args={"x"}, device_types="cpu")
        >>> def numpy_sin_inplace(x: Tensor) -> None:
        >>>     x_np = x.numpy()
        >>>     np.sin(x_np, out=x_np)
        >>>
        >>> x = torch.randn(3)
        >>> expected = x.sin()
        >>> numpy_sin_inplace(x)
        >>> assert torch.allclose(x, expected)
        >>>
        >>> # Example of a factory function
        >>> @torch.library.custom_op("mylib::bar", mutates_args={}, device_types="cpu")
        >>> def bar(device: torch.device) -> Tensor:
        >>>     return torch.ones(3)
        >>>
        >>> bar("cpu")
        >>>
        >>> # Example of a custom op with list inputs
        >>> @custom_op("mylib::weighted_sum", mutates_args=())
        >>> def weighted_sum(
        >>>     tensors: list[Tensor],
        >>>     weights: list[float],
        >>> ) -> Tensor:
        >>>     return sum(t * w for t, w in zip(tensors, weights))
        >>>
        >>> x = torch.randn(3)
        >>> y = torch.randn(3)
        >>> out = weighted_sum([x, y], [0.3, 0.7])

    """

    def inner(fn: Callable[..., object]) -> CustomOpDef:
        import torch

        if schema is None:
            schema_str = torch.library.infer_schema(fn, mutates_args=mutates_args)
        else:
            schema_str = schema

        namespace, opname = name.split("::")
        result = CustomOpDef(namespace, opname, schema_str, fn, tags)
        if schema is not None:
            # Check that schema's alias annotations match those of `mutates_args`.
            expected = set()
            for arg in result._opoverload._schema.arguments:
                if arg.alias_info is not None and arg.alias_info.is_write:
                    expected.add(arg.name)
            if expected != set(mutates_args):
                raise ValueError(
                    f"Attempted to create a custom op with `mutates_args={mutates_args}` "
                    f"and `schema={schema}. The schema suggests that the op mutates {expected}"
                    f"which is different from what was provided to us in `mutates_args`. "
                    f"Please make these consistent."
                )
        result.register_kernel(device_types)(fn)
        return result

    if fn is None:
        return inner
    return inner(fn)


def custom_op(opname, symbolic_fn, opset_version):
    """Context manager/decorator to test ONNX export with custom operator"""
    try:
        register_custom_op_symbolic(opname, symbolic_fn, opset_version)
        yield
    finally:
        unregister_custom_op_symbolic(opname, opset_version)


def custom_op(
    arg_types: list[RType],
    return_type: RType,
    c_function_name: str,
    error_kind: int,
    var_arg_type: RType | None = None,
    truncated_type: RType | None = None,
    ordering: list[int] | None = None,
    extra_int_constants: list[tuple[int, RType]] | None = None,
    steals: StealsDescription = False,
    is_borrowed: bool = False,
    *,
    is_pure: bool = False,
    returns_null: bool = False,
) -> CFunctionDescription:
    """Create a one-off CallC op that can't be automatically generated from the AST.

    Most arguments are similar to method_op().
    """
    if extra_int_constants is None:
        extra_int_constants = []
    return CFunctionDescription(
        "<custom>",
        arg_types,
        return_type,
        var_arg_type,
        truncated_type,
        c_function_name,
        error_kind,
        steals,
        is_borrowed,
        ordering,
        extra_int_constants,
        0,
        is_pure=is_pure,
        returns_null=returns_null,
        dependencies=None,
    )

