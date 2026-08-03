import functools
from typing import Callable

def wrap_numpy(fn):
    r"""Decorator that turns a function from ``np.ndarray``s to ``np.ndarray``s into a function
    from ``torch.Tensor``s to ``torch.Tensor``s.

    It is designed to be used with :func:`torch.compile` with ``fullgraph=True``. It allows to
    compile a NumPy function as if it were a PyTorch function. This allows you to run NumPy code
    on CUDA or compute its gradients.

    .. note::

        This decorator does not work without :func:`torch.compile`.

    Example::

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CUDA)
        >>> # Compile a NumPy function as a Tensor -> Tensor function
        >>> @torch.compile(fullgraph=True)
        >>> @torch.compiler.wrap_numpy
        >>> def fn(a: np.ndarray):
        >>>     return np.sum(a * a)
        >>> # Execute the NumPy function using Tensors on CUDA and compute the gradients
        >>> x = torch.arange(6, dtype=torch.float32, device="cuda", requires_grad=True)
        >>> out = fn(x)
        >>> out.backward()
        >>> print(x.grad)
        tensor([ 0.,  2.,  4.,  6.,  8., 10.], device='cuda:0')
    """
    from torch._dynamo.external_utils import wrap_numpy as wrap

    return wrap(fn)


def wrap_numpy(f: Callable[_P, _R]) -> Callable[_P, _R]:
    r"""Decorator that turns a function from ``np.ndarray``s to ``np.ndarray``s into a function
    from ``torch.Tensor``s to ``torch.Tensor``s.
    """
    if not np:
        return f

    @functools.wraps(f)
    def wrap(*args: _P.args, **kwargs: _P.kwargs) -> pytree.PyTree:
        args, kwargs = pytree.tree_map_only(
            torch.Tensor, lambda x: x.numpy(), (args, kwargs)
        )
        out = f(*args, **kwargs)
        # pyrefly: ignore [missing-attribute]
        return pytree.tree_map_only(np.ndarray, lambda x: torch.as_tensor(x), out)

    return wrap

