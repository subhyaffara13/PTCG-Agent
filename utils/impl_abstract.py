
def impl_abstract(qualname, func=None, *, lib=None, _stacklevel=1):
    r"""This API was renamed to :func:`torch.library.register_fake` in PyTorch 2.4.
    Please use that instead.
    """
    if func is not None:
        _stacklevel = _stacklevel + 1
    return register_fake(qualname, func, lib=lib, _stacklevel=_stacklevel)


def impl_abstract(qualname, *, func=None):
    r"""Register an abstract implementation for this operator.

    An "abstract implementation" specifies the behavior of this operator on
    Tensors that carry no data. Given some input Tensors with certain properties
    (sizes/strides/storage_offset/device), it specifies what the properties of
    the output Tensors are.

    The abstract implementation has the same signature as the operator.
    It is run for both FakeTensors and meta tensors. To write an abstract
    implementation, assume that all Tensor inputs to the operator are
    regular CPU/CUDA/Meta tensors, but they do not have storage, and
    you are trying to return regular CPU/CUDA/Meta tensor(s) as output.
    The abstract implementation must consist of only PyTorch operations
    (and may not directly access the storage or data of any input or
    intermediate Tensors).

    This API may be used as a decorator (see examples).

    For a detailed guide on custom ops, please see
    https://docs.google.com/document/d/1aGWtgxV3HppuxQAdddyPrs74_aEntpkYt9MalnCKnhk

    Examples::
        >>> import numpy as np
        >>> from torch import Tensor
        >>>
        >>> # Example 1: an operator without data-dependent output shape
        >>> @torch._custom_ops.custom_op("mylibrary::custom_linear")
        >>> def custom_linear(x: Tensor, weight: Tensor, bias: Tensor) -> Tensor:
        >>>     raise NotImplementedError
        >>>
        >>> @torch._custom_ops.impl_abstract("mylibrary::custom_linear")
        >>> def custom_linear_abstract(x, weight):
        >>>     assert x.dim() == 2
        >>>     assert weight.dim() == 2
        >>>     assert bias.dim() == 1
        >>>     assert x.shape[1] == weight.shape[1]
        >>>     assert weight.shape[0] == bias.shape[0]
        >>>     assert x.device == weight.device
        >>>
        >>>     return (x @ weight.t()) + bias
        >>>
        >>> # Example 2: an operator with data-dependent output shape
        >>> @torch._custom_ops.custom_op('mylibrary::custom_nonzero')
        >>> def custom_nonzero(x: Tensor) -> Tensor:
        >>>     ...
        >>>
        >>> @torch._custom_ops.impl_abstract("mylibrary::custom_nonzero")
        >>> def custom_nonzero_abstract(x):
        >>>     # Number of nonzero-elements is data-dependent.
        >>>     # Since we cannot peek at the data in an abstract impl,
        >>>     # we use the ctx object to construct a new symint that
        >>>     # represents the data-dependent size.
        >>>     ctx = torch._custom_ops.get_ctx()
        >>>     nnz = ctx.create_unbacked_symint()
        >>>     shape = [x.dim(), nnz]
        >>>     result = x.new_empty(shape, dtype=torch.long)
        >>>     return result
        >>>
        >>> @torch._custom_ops.impl("mylibrary::custom_nonzero")
        >>> def custom_nonzero_impl(x):
        >>>     x_np = to_numpy(x)
        >>>     res = np.stack(np.nonzero(x_np), axis=1)
        >>>     # unbacked symbolic ints in PyTorch must be >= 2, so we
        >>>     # constrain the range to at least 2
        >>>     if res.shape[0] <= 1:
        >>>         raise RuntimeError("not supported")
        >>>     return torch.tensor(res, device=x.device)

    """
    import torch.library

    return torch.library.register_fake(qualname, func, _stacklevel=2)

