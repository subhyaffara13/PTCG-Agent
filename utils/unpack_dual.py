
def unpack_dual(tensor, *, level=None):
    r"""Unpack a "dual tensor" to get both its Tensor value and its forward AD gradient.

    The result is a namedtuple ``(primal, tangent)`` where ``primal`` is a view of
    :attr:`tensor`'s primal and ``tangent`` is :attr:`tensor`'s tangent as-is.
    Neither of these tensors can be dual tensor of level :attr:`level`.

    This function is backward differentiable.

    Example::

        >>> # xdoctest: +SKIP("Undefined variables")
        >>> with dual_level():
        ...     inp = make_dual(x, x_t)
        ...     out = f(inp)
        ...     y, jvp = unpack_dual(out)
        ...     jvp = unpack_dual(out).tangent

    Please see the `forward-mode AD tutorial <https://pytorch.org/tutorials/intermediate/forward_ad_usage.html>`__
    for detailed steps on how to use this API.
    """
    if level is None:
        level = _current_level

    if level < 0:
        return UnpackedDualTensor(tensor, None)

    primal, dual = torch._VF._unpack_dual(tensor, level=level)

    return UnpackedDualTensor(primal, dual)

