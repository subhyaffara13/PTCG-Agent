
def logaddexp(
    input: Tensor | MaskedTensor,
    other: Tensor | MaskedTensor,
    *,
    dtype: DType | None = None,
    input_mask: Tensor | None = None,
    other_mask: Tensor | None = None,
) -> Tensor:
    """logaddexp(input, other, *, dtype=None, input_mask=None, other_mask=None) -> Tensor

    Returns logaddexp of all the elements in the :attr:`input` and the :attr:`other`
    tensor. The :attr:`input` elements are masked out according to the boolean tensor
    :attr:`input_mask` and the attr:`other` elements are masked out according to the boolean tensor
    :attr:`other_mask`.

    The shapes of a mask tensor and the tensor to be masked
    don't need to match, but they must be :ref:`broadcastable
    <broadcasting-semantics>` and the dimensionality of the mask
    tensor must not be greater than of the tensor to be masked.

    Args:
        input (Tensor): the input tensor
        other (Tensor): the second input tensor

    Keyword args:
        dtype (:class:`torch.dtype`, optional): the desired data type
          of returned tensor.  If specified, the output tensor is
          casted to :attr:`dtype` after the operation is
          performed. Default: None.
        input_mask (:class:`torch.Tensor`, optional): the boolean tensor
          containing the binary mask of validity of :attr:`input` tensor elements.
          Default: None that is equivalent to ``torch.ones(input.shape, dtype=torch.bool)``.
        other_mask (:class:`torch.Tensor`, optional): the boolean tensor
          containing the binary mask of validity of :attr:`other` tensor elements.
          Default: None that is equivalent to ``torch.ones(other.shape, dtype=torch.bool)``.

    Example::

        >>> input = torch.tensor([-100.0, -200, -300])
        >>> input
        tensor([-100., -200., -300.])
        >>> other = torch.tensor([-1.0, -2, -3])
        >>> other
        tensor([-1., -2., -3.])
        >>> mask = torch.tensor([True, False, True])
        >>> mask
        tensor([ True, False,  True])
        >>> torch.masked._ops.logaddexp(input, other, input_mask=mask, other_mask=mask)
        tensor([-1., -inf, -3.])"""
    if dtype is None:
        dtype = input.dtype
    if input.layout == torch.strided and other.layout == torch.strided:
        mask_input = _combine_input_and_mask(logaddexp, input, input_mask)
        mask_other = _combine_input_and_mask(logaddexp, other, other_mask)
        return torch.logaddexp(mask_input, mask_other).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked logaddexp expects strided tensors (got {input.layout} tensor for input, {other.layout} for other)"
        )


def logaddexp(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    # Nb. this implementation does not distribute the gradients evenly when a == b
    mask = torch.real(a) >= torch.real(b)
    max_ = torch.where(mask, a, b)
    min_ = torch.where(mask, b, a)
    inf_mask = torch.logical_and(
        torch.logical_not(torch.isfinite(torch.real(a))), torch.real(a) == torch.real(b)
    )
    if utils.is_complex_dtype(a.dtype) or utils.is_complex_dtype(b.dtype):
        # are you wondering what this bunch of codes are for? edge cases!
        neg_min_mask = torch.real(min_) < 0
        inf_vals = torch.where(
            neg_min_mask, min_, torch.log(torch.exp(min_) + torch.exp(max_))
        )
        non_nan_vals = torch.where(
            inf_mask, inf_vals, max_ + torch.log1p(torch.exp(min_ - max_))
        )
        # the type for full_like does not include tensor yet
        nan_mask = torch.isnan(min_)
        return torch.where(nan_mask, complex(float("nan"), float("nan")), non_nan_vals)  # type: ignore[call-overload]
    else:
        return torch.where(inf_mask, a, max_ + torch.log1p(torch.exp(min_ - max_)))


def logaddexp(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Compute log(exp(x1) + exp(x2)) avoiding overflow."""
  x1_arr = lax.asarray(x1)
  x2_arr = lax.asarray(x2)
  assert x1_arr.dtype == x2_arr.dtype

  amax = lax.max(x1_arr, x2_arr)
  if dtypes.isdtype(x1_arr.dtype, "real floating"):
    delta = lax.sub(x1_arr, x2_arr)
    return lax.select(lax._isnan(delta),
                      lax.add(x1_arr, x2_arr),  # NaNs or infinities of the same sign.
                      lax.add(amax, lax.log1p(lax.exp(lax.neg(lax.abs(delta))))))
  elif dtypes.isdtype(x1_arr.dtype, "complex floating"):
    delta = lax.sub(lax.add(x1, x2), lax.mul(amax, lax._const(amax, 2)))
    out = lax.add(amax, lax.log1p(lax.exp(delta)))
    return lax.complex(lax.real(out), _wrap_between(lax.imag(out), np.pi))
  else:
    raise ValueError(f"logaddexp requires floating-point or complex inputs; got {x1_arr.dtype}")


def logaddexp(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Compute ``log(exp(x1) + exp(x2))`` avoiding overflow.

  JAX implementation of :obj:`numpy.logaddexp`

  Args:
    x1: input array
    x2: input array

  Returns:
    array containing the result.

  Examples:

  >>> x1 = jnp.array([1, 2, 3])
  >>> x2 = jnp.array([4, 5, 6])
  >>> result1 = jnp.logaddexp(x1, x2)
  >>> result2 = jnp.log(jnp.exp(x1) + jnp.exp(x2))
  >>> print(jnp.allclose(result1, result2))
  True
  """
  x1, x2 = promote_args_inexact("logaddexp", x1, x2)
  return lax_other.logaddexp(x1, x2)

