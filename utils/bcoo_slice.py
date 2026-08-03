import math


def bcoo_slice(mat: BCOO, *, start_indices: Sequence[int], limit_indices: Sequence[int],
               strides: Sequence[int] | None = None) -> BCOO:
  """Sparse implementation of :func:`jax.lax.slice`.

  Args:
    mat: BCOO array to be reshaped.
    start_indices: sequence of integers of length `mat.ndim` specifying the starting
      indices of each slice.
    limit_indices: sequence of integers of length `mat.ndim` specifying the ending
      indices of each slice
    strides: (not implemented) sequence of integers of length `mat.ndim` specifying
      the stride for each slice

  Returns:
    out: BCOO array containing the slice.
  """
  if not isinstance(mat, BCOO):
    raise TypeError(f"bcoo_slice: input should be BCOO array, got type(mat)={type(mat)}")
  start_indices = [operator.index(i) for i in start_indices]
  limit_indices = [operator.index(i) for i in limit_indices]
  if strides is not None:
    strides = [operator.index(i) for i in strides]
  else:
    strides = [1] * mat.ndim
  if len(start_indices) != len(limit_indices) != len(strides) != mat.ndim:
    raise ValueError(f"bcoo_slice: indices must have size mat.ndim={mat.ndim}")
  if len(strides) != mat.ndim:
    raise ValueError(f"len(strides) = {len(strides)}; expected {mat.ndim}")
  if any(s <= 0 for s in strides):
    raise ValueError(f"strides must be a sequence of positive integers; got {strides}")

  if not all(0 <= start <= end <= size
             for start, end, size in safe_zip(start_indices, limit_indices, mat.shape)):
    raise ValueError(f"bcoo_slice: invalid indices. Got {start_indices=}, "
                     f"{limit_indices=} and shape={mat.shape}")

  start_batch, start_sparse, start_dense = split_list(start_indices, [mat.n_batch, mat.n_sparse])
  end_batch, end_sparse, end_dense = split_list(limit_indices, [mat.n_batch, mat.n_sparse])
  stride_batch, stride_sparse, stride_dense = split_list(strides, [mat.n_batch, mat.n_sparse])

  data_slices = []
  index_slices = []
  for i, (start, end, stride) in enumerate(zip(start_batch, end_batch, stride_batch)):
    data_slices.append(slice(None) if mat.data.shape[i] != mat.shape[i] else slice(start, end, stride))
    index_slices.append(slice(None) if mat.indices.shape[i] != mat.shape[i] else slice(start, end, stride))
  data_slices.append(slice(None))
  index_slices.extend([slice(None), slice(None)])
  for i, (start, end, stride) in enumerate(zip(start_dense, end_dense, stride_dense)):
    data_slices.append(slice(start, end, stride))
  new_data = mat.data[tuple(data_slices)]
  new_indices = mat.indices[tuple(index_slices)]
  new_shape = tuple(
    (end - start + stride - 1) // stride
    for start, end, stride in safe_zip(start_indices, limit_indices, strides))
  _, new_shape_sparse, _ = split_list(new_shape, [mat.n_batch, mat.n_sparse])

  if mat.n_sparse:
    starts = jnp.expand_dims(jnp.array(start_sparse, dtype=new_indices.dtype), range(mat.n_batch + 1))
    ends = jnp.expand_dims(jnp.array(end_sparse, dtype=new_indices.dtype), range(mat.n_batch + 1))
    strides_ = jnp.expand_dims(jnp.array(stride_sparse, dtype=new_indices.dtype), range(mat.n_batch + 1))

    keep = jnp.all((new_indices >= starts) & (new_indices < ends) &
                   ((new_indices - starts) % strides_ == 0),
                   axis=-1, keepdims=True)
    new_indices = jnp.where(keep, (new_indices - starts + strides_ - 1) // strides_,
                            (ends - starts + strides_ - 1) // strides_)

    keep_data = lax.expand_dims(keep[..., 0], range(mat.n_batch + 1, mat.n_batch + 1 + mat.n_dense))
    new_data = jnp.where(keep_data, new_data, 0)

    new_nse = math.prod(new_shape_sparse)
    if mat.nse > new_nse:
      new_data, new_indices = _bcoo_sum_duplicates(
        new_data, new_indices, spinfo=SparseInfo(shape=new_shape), nse=new_nse)

  return BCOO((new_data, new_indices), shape=new_shape)

