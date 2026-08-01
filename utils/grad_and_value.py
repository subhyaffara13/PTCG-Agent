
def grad_and_value(
    func: Callable[_P, Any], argnums: argnums_t = 0, has_aux: bool = False
) -> Callable[_P, tuple[Any, Any]]:
    """
    Returns a function to compute a tuple of the gradient and primal, or
    forward, computation.

    Args:
        func (Callable): A Python function that takes one or more arguments.
            Must return a single-element Tensor. If specified ``has_aux``
            equals ``True``, function can return a tuple of single-element
            Tensor and other auxiliary objects: ``(output, aux)``.
        argnums (int or Tuple[int]): Specifies arguments to compute gradients
            with respect to. ``argnums`` can be single integer or tuple of
            integers. Default: 0.
        has_aux (bool): Flag indicating that ``func`` returns a tensor and
            other auxiliary objects: ``(output, aux)``. Default: False.

    Returns:
        Function to compute a tuple of gradients with respect to its inputs
        and the forward computation. By default, the output of the function is
        a tuple of the gradient tensor(s) with respect to the first argument
        and the primal computation. If specified ``has_aux`` equals
        ``True``, tuple of gradients and tuple of the forward computation with
        output auxiliary objects is returned. If ``argnums`` is a tuple of
        integers, a tuple of a tuple of the output gradients with respect to
        each ``argnums`` value and the forward computation is returned.

    See :func:`grad` for examples
    """
    from torch._functorch import eager_transforms
    from torch.compiler import is_compiling

    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> tuple[Any, torch.Tensor]:
        return eager_transforms.grad_and_value_impl(
            func, argnums, has_aux, args, kwargs
        )

    if not is_compiling():
        wrapper = functools.wraps(func)(wrapper)

    return wrapper


def grad_and_value(
    func: Callable[..., Any], argnums: argnums_t = 0, has_aux: bool = False
) -> Callable[..., Any]:
    warn_deprecated("grad_and_value")
    return apis.grad_and_value(func, argnums, has_aux)

