
def bcoo_dynamic_slice(mat: BCOO, start_indices: Sequence[Any], slice_sizes: Sequence[int]) -> BCOO:
  """Sparse implementation of :func:`jax.lax.dynamic_slice`.

  Args:
    mat: BCOO array to slice.
    start_indices: a list of scalar indices, one per dimension. These values
      may be dynamic.
    slice_sizes: the size of the slice. Must be a sequence of non-negative
      integers with length equal to `ndim(operand)`. Inside a JIT compiled
      function, only static values are supported (all JAX arrays inside JIT
      must have statically known size).

  Returns:
    out: BCOO array containing the slice.
  """
  slice_sizes = tuple(operator.index(i) for i in slice_sizes)
  # Use abstract eval to validate inputs.
  jax.jit(lax.dynamic_slice, static_argnames=("slice_sizes",)).eval_shape(
          jax.ShapeDtypeStruct(mat.shape, mat.dtype), start_indices,
          slice_sizes=slice_sizes)
  if not isinstance(mat, BCOO):
    raise TypeError(f"bcoo_slice: input should be BCOO array, got type(mat)={type(mat)}")
  start_indices = tuple(jnp.asarray(i) for i in start_indices)
  assert all(jnp.issubdtype(i.dtype, np.integer) for i in start_indices)
  assert all(i.shape == () for i in start_indices)
  if len(start_indices) != len(slice_sizes) != mat.ndim:
    raise ValueError(f"bcoo_dynamic_slice: indices must have size mat.ndim={mat.ndim}")
  if not all(0 <= slice_size <= axis_size for slice_size, axis_size in zip(slice_sizes, mat.shape)):
    raise TypeError("slice_sizes must be less than or equal to operand shape, "
                    f"got slice_sizes {slice_sizes} for operand shape {mat.shape}")

  start_batch, start_sparse, start_dense = split_list(start_indices, [mat.n_batch, mat.n_sparse])
  size_batch, size_sparse, size_dense = split_list(slice_sizes, [mat.n_batch, mat.n_sparse])

  data_start = []
  data_sizes = []
  indices_start = []
  indices_sizes = []
  zero = _const(start_indices[0] if start_indices else np.int32, 0)
  for i, (start, size) in enumerate(zip(start_batch, size_batch)):
    data_is_broadcast = mat.data.shape[i] != mat.shape[i]
    indices_is_broadcast = mat.indices.shape[i] != mat.shape[i]
    data_start.append(zero if data_is_broadcast else start)
    data_sizes.append(1 if data_is_broadcast else size)
    indices_start.append(zero if indices_is_broadcast else start)
    indices_sizes.append(1 if indices_is_broadcast else size)
  data_start.append(zero)
  data_sizes.append(mat.nse)
  indices_start.extend([zero, zero])
  indices_sizes.extend([mat.nse, mat.n_sparse])
  data_start.extend(start_dense)
  data_sizes.extend(size_dense)

  new_data = lax.dynamic_slice(mat.data, data_start, data_sizes)
  new_indices = lax.dynamic_slice(mat.indices, indices_start, indices_sizes)
  new_shape = slice_sizes

  if mat.n_sparse:
    starts = jnp.array(start_sparse, dtype=new_indices.dtype)
    sizes = jnp.array(size_sparse, dtype=new_indices.dtype)
    sparse_shape = jnp.array(mat.shape[mat.n_batch: mat.n_batch + mat.n_sparse], dtype=new_indices.dtype)
    starts = jnp.where(starts < 0, starts + sparse_shape, starts)
    starts = jnp.clip(starts, 0, sparse_shape - sizes)

    starts = jnp.expand_dims(starts, range(mat.n_batch + 1))
    sizes = jnp.expand_dims(sizes, range(mat.n_batch + 1))
    sparse_shape = jnp.expand_dims(sparse_shape, range(mat.n_batch + 1))

    keep = jnp.all((new_indices >= starts) & (new_indices < starts + sizes), -1, keepdims=True)
    new_indices = jnp.where(keep, new_indices - starts, sizes)

    keep_data = lax.expand_dims(keep[..., 0], range(mat.n_batch + 1, mat.n_batch + 1 + mat.n_dense))
    new_data = jnp.where(keep_data, new_data, 0)

    if mat.nse > math.prod(size_sparse):
      new_nse = math.prod(size_sparse)
      new_data, new_indices = _bcoo_sum_duplicates(
        new_data, new_indices, spinfo=SparseInfo(shape=new_shape), nse=new_nse)

  return BCOO((new_data, new_indices), shape=new_shape)

