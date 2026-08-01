
def _where(mask: Tensor, input: Tensor, fill_value: Tensor) -> Tensor:
    """torch.where with sparse inputs support.

    _where implements the following invariant:

      _where(mask, input, fill_value).to_dense(fill_value) ==
        torch.where(mask.to_dense(), input.to_dense(), torch.full(input.shape, fill_value))

    where `a == b` means `assertEqual(a, b)`, mask is boolean sparse
    tensor, and `to_dense(fill_value)` is like `to_dense()` except
    that the unspecified elements are mapped to `fill_value` rather
    than to `0`.

    Returns a sparse tensor with the following features:

    - all specified elements correspond to masked-in elements that
      have the values of the input tensor. If there exists a masked-in
      element (as specified by mask) that is not specified in the
      input, in the result tensor, the corresponding element has value
      0. In the dense part of the sparse tensor, the masked-out
      elements are replaced with fill_value.

    - all unspecified elements correspond to masked-out elements.
    """
    if mask.layout == torch.strided:
        return torch.where(mask, input, fill_value)
    elif mask.layout == torch.sparse_coo:
        return _sparse_coo_where(mask, input, fill_value)
    elif mask.layout == torch.sparse_csr:
        return _sparse_csr_where(mask, input, fill_value)
    else:
        raise ValueError(
            f"_where expects strided or sparse COO or sparse CSR tensor but got {mask.layout}"
        )


def _where(condition: ArrayLike, x: ArrayLike, y: ArrayLike) -> Array:
  condition, x, y = ensure_arraylike("where", condition, x, y)
  if x is None or y is None:
    raise ValueError("Either both or neither of the x and y arguments should "
                     "be provided to jax.numpy.where, got {} and {}."
                     .format(x, y))
  if not np.issubdtype(_dtype(condition), np.bool_):
    condition = lax.ne(condition, lax._zero(condition))
  x, y = promote_dtypes(x, y)
  if np.ndim(condition) == 0:
    # lax.select() handles scalar conditions without broadcasting.
    x_arr, y_arr = _broadcast_arrays(x, y)
  else:
    condition, x_arr, y_arr = _broadcast_arrays(condition, x, y)
  try:
    is_always_empty = core.is_empty_shape(x_arr.shape)
  except:
    is_always_empty = False  # can fail with dynamic shapes
  return lax.select(condition, x_arr, y_arr) if not is_always_empty else x_arr

