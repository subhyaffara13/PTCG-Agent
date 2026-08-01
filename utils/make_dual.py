
def make_dual(tensor, tangent, *, level=None):
    r"""Associate a tensor value with its tangent to create a "dual tensor" for forward AD gradient computation.

    The result is a new tensor aliased to :attr:`tensor` with :attr:`tangent` embedded
    as an attribute as-is if it has the same storage layout or copied otherwise.
    The tangent attribute can be recovered with :func:`unpack_dual`.

    This function is backward differentiable.

    Given a function `f` whose jacobian is `J`, it allows one to compute the Jacobian-vector product (`jvp`)
    between `J` and a given vector `v` as follows.

    Example::

        >>> # xdoctest: +SKIP("Undefined variables")
        >>> with dual_level():
        ...     inp = make_dual(x, v)
        ...     out = f(inp)
        ...     y, jvp = unpack_dual(out)

    Please see the `forward-mode AD tutorial <https://pytorch.org/tutorials/intermediate/forward_ad_usage.html>`__
    for detailed steps on how to use this API.

    """
    # See NOTE: [forward-mode AD decompositions mechanism]
    #
    # Import from torch._decomp import decompositions_for_jvp to register
    # decompositions for jvp to the jit registry
    #
    # FIXME: We specify that __debug__ must be True because
    # if python is run with -OO or -O flags (i.e., __debug__ is False), we encounter the
    # following error:
    #
    # Return value was annotated as having type Tuple[NoneType, NoneType] but is actually of
    # type Tuple[Tensor, Tensor]:
    #   File ".../torch/_decomp/__init__.py", line 1585
    #     else:
    #         buffer = z
    #     return min - torch.log1p(z), buffer
    #     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ <--- HERE
    _maybe_load_decompositions()

    if level is None:
        level = _current_level

    if level < 0:
        raise RuntimeError(
            "Trying to create a dual Tensor for forward AD but no level "
            "exists, make sure to enter_dual_level() first."
        )
    if not (tensor.is_floating_point() or tensor.is_complex()):
        raise ValueError(
            f"Expected primal to be floating point or complex, but got: {tensor.dtype}"
        )
    if not (tangent.is_floating_point() or tangent.is_complex()):
        raise ValueError(
            f"Expected tangent to be floating point or complex, but got: {tangent.dtype}"
        )

    return torch._VF._make_dual(tensor, tangent, level=level)

