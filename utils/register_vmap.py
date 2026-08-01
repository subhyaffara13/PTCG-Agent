
def register_vmap(
    op: _op_identifier,
    func: Callable | None = None,
    /,
    *,
    lib=None,
):
    r"""Register a vmap implementation to support :func:`torch.vmap` for this custom op.

    This API may be used as a decorator (see examples).

    In order for an operator to work with :func:`torch.vmap`, you may need to register a
    vmap implementation in the following signature:

        ``vmap_func(info, in_dims: Tuple[Optional[int]], *args, **kwargs)``,

    where ``*args`` and ``**kwargs`` are the arguments and kwargs for ``op``.
    We do not support kwarg-only Tensor args.

    It specifies how do we compute the batched version of ``op`` given inputs with an additional
    dimension (specified by ``in_dims``).

    For each arg in ``args``, ``in_dims`` has a corresponding ``Optional[int]``. It is ``None``
    if the arg is not a Tensor or if the arg is not being vmapped over, otherwise, it is an integer
    specifying what dimension of the Tensor is being vmapped over.

    ``info`` is a collection of additional metadata that may be helpful:
    ``info.batch_size`` specifies the size of the dimension being vmapped over, while
    ``info.randomness`` is the ``randomness`` option that was passed to :func:`torch.vmap`.

    The return of the function ``func`` is a tuple of ``(output, out_dims)``. Similar to ``in_dims``,
    ``out_dims`` should be of the same structure as ``output`` and contain one ``out_dim``
    per output that specifies if the output has the vmapped dimension and what index it is in.

    Examples:
        >>> import torch
        >>> import numpy as np
        >>> from torch import Tensor
        >>> from typing import Tuple
        >>>
        >>> def to_numpy(tensor):
        >>>     return tensor.cpu().numpy()
        >>>
        >>> lib = torch.library.Library("mylib", "FRAGMENT")
        >>> @torch.library.custom_op("mylib::numpy_cube", mutates_args=())
        >>> def numpy_cube(x: Tensor) -> Tuple[Tensor, Tensor]:
        >>>     x_np = to_numpy(x)
        >>>     dx = torch.tensor(3 * x_np ** 2, device=x.device)
        >>>     return torch.tensor(x_np ** 3, device=x.device), dx
        >>>
        >>> def numpy_cube_vmap(info, in_dims, x):
        >>>     result = numpy_cube(x)
        >>>     return result, (in_dims[0], in_dims[0])
        >>>
        >>> torch.library.register_vmap(numpy_cube, numpy_cube_vmap)
        >>>
        >>> x = torch.randn(3)
        >>> torch.vmap(numpy_cube)(x)
        >>>
        >>> @torch.library.custom_op("mylib::numpy_mul", mutates_args=())
        >>> def numpy_mul(x: Tensor, y: Tensor) -> Tensor:
        >>>     return torch.tensor(to_numpy(x) * to_numpy(y), device=x.device)
        >>>
        >>> @torch.library.register_vmap("mylib::numpy_mul")
        >>> def numpy_mul_vmap(info, in_dims, x, y):
        >>>     x_bdim, y_bdim = in_dims
        >>>     x = x.movedim(x_bdim, -1) if x_bdim is not None else x.unsqueeze(-1)
        >>>     y = y.movedim(y_bdim, -1) if y_bdim is not None else y.unsqueeze(-1)
        >>>     result = x * y
        >>>     result = result.movedim(-1, 0)
        >>>     return result, 0
        >>>
        >>>
        >>> x = torch.randn(3)
        >>> y = torch.randn(3)
        >>> torch.vmap(numpy_mul)(x, y)

    .. note::
        The vmap function should aim to preserve the semantics of the entire custom operator.
        That is, ``grad(vmap(op))`` should be replaceable with a ``grad(map(op))``.

        If your custom operator has any custom behavior in the backward pass, please
        keep this in mind.

    """
    if not isinstance(
        op, (str, torch._ops.OpOverload, torch._library.custom_ops.CustomOpDef)
    ):
        raise ValueError(f"register_vmap({op}): got unexpected type for op: {type(op)}")
    if isinstance(op, torch._ops.OpOverload):
        op = op._name
    opdef = _maybe_get_opdef(op)
    if opdef is not None:
        return opdef.register_vmap(func)
    if not isinstance(op, str):
        raise AssertionError(f"op must be str at this point, got {type(op).__name__}")
    qualname = op
    op = torch._library.utils.lookup_op(qualname)
    schema = op._schema
    if _library.utils.has_kwarg_only_tensors(schema):
        raise NotImplementedError(
            f"register_vmap with kwarg-only Tensor args. In the original "
            f"definition of the op, please make your tensors not kwarg-only. "
            f"Got: {schema}"
        )

    def register(func):
        nonlocal op, lib

        namespace, opname = torch._library.utils.parse_namespace(qualname)
        if lib is None:
            lib = Library(namespace, "FRAGMENT")
            _keep_alive.append(lib)

        from torch._functorch.autograd_function import custom_function_call_vmap_helper
        from torch._functorch.pyfunctorch import retrieve_current_functorch_interpreter

        def wrapped_func(keyset, *args, **kwargs):
            interpreter = retrieve_current_functorch_interpreter()
            return custom_function_call_vmap_helper(
                # pyrefly: ignore[bad-argument-type]
                interpreter,
                func,
                op,
                *args,
                **kwargs,
            )

        lib.impl(opname, wrapped_func, "FuncTorchBatched", with_keyset=True)

    if func is None:
        return register
    else:
        return register(func)

