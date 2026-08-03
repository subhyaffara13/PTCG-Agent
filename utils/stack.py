import logging
import re
from typing import Any

def stack(tensors: list[list[int]], dim: int):
    unsqueezed_tensors: list[list[int]] = []
    for tensor in tensors:
        unsqueezed = unsqueeze(tensor, dim)
        unsqueezed_tensors.append(unsqueezed)
    return cat(unsqueezed_tensors, dim)


def stack(
    arrays: Sequence[ArrayLike],
    axis=0,
    out: OutArray | None = None,
    *,
    dtype: DTypeLike | None = None,
    casting: CastingModes | None = "same_kind",
):
    _concat_check(arrays, dtype, out=out)

    tensors = _concat_cast_helper(arrays, dtype=dtype, casting=casting)
    result_ndim = tensors[0].ndim + 1
    axis = _util.normalize_axis_index(axis, result_ndim)
    return torch.stack(tensors, axis=axis)


def stack(tensors: TensorSequenceType, dim: int = 0) -> TensorLikeType:
    if len(tensors) == 0:
        raise AssertionError("stack expects a non-empty TensorList")
    wrapped_dim = utils.canonicalize_dim(tensors[0].ndim + 1, dim)
    # Refs need sparse support to check other condition
    if wrapped_dim < tensors[0].ndim:  # and not tensors[0].is_sparse:
        _check_stack_inputs(tensors)
        result_sizes = list(tensors[0].shape)
        result_sizes.insert(wrapped_dim, len(tensors))
        out = torch.cat(tensors, wrapped_dim)
        return out.view(result_sizes)

    # If dim == tensors[0].ndim, view cannot efficiently handle it
    return torch.cat([t.unsqueeze(wrapped_dim) for t in tensors], dim)


def stack(g: jit_utils.GraphContext, tensor_list, dim):
    if symbolic_helper._is_packed_list(tensor_list):
        return opset9.stack(g, tensor_list, dim)
    else:
        dim = symbolic_helper._get_const(dim, "i", "dim")
        return g.op("ConcatFromSequence", tensor_list, axis_i=dim, new_axis_i=1)


def stack(g: jit_utils.GraphContext, tensor_list, dim):
    unsqueezed = [
        symbolic_helper._unsqueeze_helper(g, t, [dim])
        for t in symbolic_helper._unpack_list(tensor_list)
    ]
    return g.op("Concat", *unsqueezed, axis_i=dim)


def stack(
    frame: DataFrame, level=-1, dropna: bool = True, sort: bool = True
) -> Series | DataFrame:
    """
    Convert DataFrame to Series with multi-level Index. Columns become the
    second level of the resulting hierarchical index

    Returns
    -------
    stacked : Series or DataFrame
    """

    def stack_factorize(index):
        if index.is_unique:
            return index, np.arange(len(index))
        codes, categories = factorize_from_iterable(index)
        return categories, codes

    N, K = frame.shape

    # Will also convert negative level numbers and check if out of bounds.
    level_num = frame.columns._get_level_number(level)

    if isinstance(frame.columns, MultiIndex):
        return _stack_multi_columns(
            frame, level_num=level_num, dropna=dropna, sort=sort
        )
    elif isinstance(frame.index, MultiIndex):
        new_levels = list(frame.index.levels)
        new_codes = [lab.repeat(K) for lab in frame.index.codes]

        clev, clab = stack_factorize(frame.columns)
        new_levels.append(clev)
        new_codes.append(np.tile(clab, N).ravel())

        new_names = list(frame.index.names)
        new_names.append(frame.columns.name)
        new_index = MultiIndex(
            levels=new_levels, codes=new_codes, names=new_names, verify_integrity=False
        )
    else:
        levels, (ilab, clab) = zip(
            *map(stack_factorize, (frame.index, frame.columns)), strict=True
        )
        codes = ilab.repeat(K), np.tile(clab, N).ravel()
        new_index = MultiIndex(
            levels=levels,
            codes=codes,
            names=[frame.index.name, frame.columns.name],
            verify_integrity=False,
        )

    new_values: ArrayLike
    if not frame.empty and frame._is_homogeneous_type:
        # For homogeneous EAs, frame._values will coerce to object. So
        # we concatenate instead.
        dtypes = list(frame.dtypes._values)
        dtype = dtypes[0]

        if isinstance(dtype, ExtensionDtype):
            arr = dtype.construct_array_type()
            new_values = arr._concat_same_type(
                [col._values for _, col in frame.items()]
            )
            new_values = _reorder_for_extension_array_stack(new_values, N, K)
        else:
            # homogeneous, non-EA
            new_values = frame._values.ravel()

    else:
        # non-homogeneous
        new_values = frame._values.ravel()

    if dropna:
        mask = notna(new_values)
        new_values = new_values[mask]
        new_index = new_index[mask]

    return frame._constructor_sliced(new_values, index=new_index)


def stack(
    pattern: str,
    *,
    expected_count: int | None = None,
    axis: int = 0,
    filler_mapping: Mapping[str, float] | None = None,
    default_filler: float | None = None,
    inplace: bool = False,
    sort_by_size: bool = True,
    target_sharding: jax.sharding.Sharding | None = None,
) -> Transformation:
  r"""Stacks parameters by finding sets that match a pattern.

  The pattern must contain exactly one capture group with a positive integer,
  which is used to extract the index of the parameter in the stack. This capture
  group is removed from parameter names to form the base key for the stacked
  parameter.

  Example:
      pattern = r"mlp\.experts\.(\d+\.)"
      expected_count = 64

        Transforms:
          "layers.0.mlp.experts.0.weight": arr0
          "layers.0.mlp.experts.1.weight": arr1
          ...
          "layers.0.mlp.experts.63.weight": arr63
        Into:
          "layers.0.mlp.experts.weight": stack([arr0, arr1, ..., arr63])

  Args:
      pattern: Regex to filter keys for stacking. Must contain exactly one
        capture group, which is used to extract the index. This capture group is
        removed from parameter names to form the base key.
      expected_count: Expected number of indices to stack for each base key. If
        None, it is inferred as the maximum index found across all base keys
        plus one. If fewer items are found than expected, padding will be
        attempted. Padding requires `default_filler` or a matching entry in
        `filler_mapping` to be provided, otherwise an error will be raised.
      axis: Axis along which to stack.
      filler_mapping: Optional map from base key regex pattern to filler value.
        Used to pad missing indices. If padding is required and no filler is
        provided via this argument or `default_filler`, an error will be raised.
      default_filler: Default filler value if not in mapping. If padding is
        required and no filler is provided via this argument or
        `filler_mapping`, an error will be raised.
      inplace: If True, deletes matched keys from input params to save memory.
        Requires input params to be a dict.
      sort_by_size: If True, stacks largest parameters first to manage peak
        headroom.
      target_sharding: If not None, reshards the stacked parameter to this
        sharding.

  Returns:
      A Transformation function.
  """
  compiled_pattern = re.compile(pattern)

  def transform(
      *params: types.PyTreeOf[jax.Array],
  ) -> types.PyTreeOf[jax.Array]:
    if len(params) > 1:
      raise ValueError(
          "Can only stack parameters in a single parameter structure."
      )
    params = params[0]
    if inplace and not isinstance(params, dict):
      raise ValueError("Inplace operations require parameters to be a dict.")

    params_dict = params if isinstance(params, dict) else {}

    groups = collections.defaultdict(dict)
    unmatched = {}

    keys_to_delete = []

    for key, value in params.items():
      match = compiled_pattern.search(key)
      if not match:
        unmatched[key] = value
        continue

      if len(match.groups()) != 1:
        raise ValueError(
            "pattern must have exactly 1 capture group for the index, "
            f"got {len(match.groups())}: {pattern}."
        )

      idx_str = match.group(1)
      idx_matches = re.findall(r"\d+", idx_str)
      assert len(idx_matches) == 1, (
          "Capture group must contain exactly one single positive integer, "
          f"got {idx_str}."
      )
      idx = int(idx_matches[0])
      # Remove group 1 of pattern from the key to get the base key.
      base_key = key[: match.start(1)] + key[match.end(1) :]
      assert (
          idx not in groups[base_key]
      ), f"Duplicate index {idx} found for base_key {base_key}"
      groups[base_key][idx] = value

      if inplace:
        keys_to_delete.append(key)

    for key in keys_to_delete:
      del params_dict[key]

    if not groups:
      return unmatched

    # Determine types and stack function (use NumPy if inputs are NumPy)
    rep_val = next(iter(next(iter(groups.values())).values()))
    is_numpy = isinstance(rep_val, np.ndarray)
    ones_fn = np.ones if is_numpy else jnp.ones

    # Determine expected_count if not provided
    local_expected_count = expected_count
    if local_expected_count is None:
      local_expected_count = (
          max(max(idx_dict.keys()) for idx_dict in groups.values()) + 1
      )

    # Sort base_keys by size if requested (for peak memory optimization)
    base_keys = list(groups.keys())
    if sort_by_size:

      def _size_bytes(base_key):
        return sum(v.nbytes for v in groups[base_key].values())

      base_keys = sorted(base_keys, key=_size_bytes, reverse=True)

    result = dict(unmatched)
    for base_key in base_keys:
      idx_dict = groups.pop(base_key)

      # Determine filler
      filler_val = default_filler
      if filler_mapping:
        for p, val in filler_mapping.items():
          if re.search(p, base_key):
            filler_val = val
            break

      if filler_val is None:
        if sorted(idx_dict.keys()) != list(range(local_expected_count)):
          raise ValueError(
              f'Stacking "{base_key}": Found keys {sorted(idx_dict.keys())},'
              f" but expected indices 0..{local_expected_count - 1} when"
              " padding is disabled (no filler_mapping or default_filler was"
              " provided)."
          )
        items_to_stack = [idx_dict[i] for i in range(local_expected_count)]
        stack_fn = _select_stack_fn(items_to_stack, target_sharding)
        stacked = stack_fn(items_to_stack, axis)
        if target_sharding is not None and stack_fn in (np.stack, jnp.stack):
          stacked = jax.device_put(stacked, target_sharding)
      else:
        # Find representative shape/dtype
        rep_val = next(iter(idx_dict.values()))
        shape = list(rep_val.shape)
        shape.insert(axis, local_expected_count)
        dtype = rep_val.dtype

        # Initialize stacked array
        stacked = (ones_fn(shape, dtype=dtype) * filler_val).astype(dtype)
        if len(idx_dict) > local_expected_count:
          raise ValueError(
              f"Found {len(idx_dict)} items, but expected maximum"
              f" {local_expected_count} for {base_key}"
          )
        # Fill in values
        for idx, val in idx_dict.items():
          if idx >= local_expected_count:
            logging.warning(
                "Stacking %s: Found %d items, expected %d. Skipping index %d.",
                base_key,
                len(idx_dict),
                local_expected_count,
                idx,
            )
            continue
          slices = [slice(None)] * len(shape)
          slices[axis] = idx
          if is_numpy:
            stacked[tuple(slices)] = val
          else:
            stacked = stacked.at[tuple(slices)].set(val)

        if len(idx_dict) != local_expected_count:
          logging.warning(
              "Stacking %s: Found %d items, expected %d. Padded with %s.",
              base_key,
              len(idx_dict),
              local_expected_count,
              filler_val,
          )

        if target_sharding is not None:
          stacked = jax.device_put(stacked, target_sharding)

      result[base_key] = stacked

    return result

  return transform


def stack(arrays, axis=0, out=None, *, dtype=None, casting="same_kind"):
    """
    Join a sequence of arrays along a new axis.

    The ``axis`` parameter specifies the index of the new axis in the
    dimensions of the result. For example, if ``axis=0`` it will be the first
    dimension and if ``axis=-1`` it will be the last dimension.

    Parameters
    ----------
    arrays : sequence of ndarrays
        Each array must have the same shape. In the case of a single ndarray
        array_like input, it will be treated as a sequence of arrays; i.e.,
        each element along the zeroth axis is treated as a separate array.

    axis : int, optional
        The axis in the result array along which the input arrays are stacked.

    out : ndarray, optional
        If provided, the destination to place the result. The shape must be
        correct, matching that of what stack would have returned if no
        out argument were specified.

    dtype : str or dtype
        If provided, the destination array will have this dtype. Cannot be
        provided together with `out`.

        .. versionadded:: 1.24

    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        Controls what kind of data casting may occur. Defaults to 'same_kind'.

        .. versionadded:: 1.24


    Returns
    -------
    stacked : ndarray
        The stacked array has one more dimension than the input arrays.

    See Also
    --------
    concatenate : Join a sequence of arrays along an existing axis.
    block : Assemble an nd-array from nested lists of blocks.
    split : Split array into a list of multiple sub-arrays of equal size.
    unstack : Split an array into a tuple of sub-arrays along an axis.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng()
    >>> arrays = [rng.normal(size=(3,4)) for _ in range(10)]
    >>> np.stack(arrays, axis=0).shape
    (10, 3, 4)

    >>> np.stack(arrays, axis=1).shape
    (3, 10, 4)

    >>> np.stack(arrays, axis=2).shape
    (3, 4, 10)

    >>> a = np.array([1, 2, 3])
    >>> b = np.array([4, 5, 6])
    >>> np.stack((a, b))
    array([[1, 2, 3],
           [4, 5, 6]])

    >>> np.stack((a, b), axis=-1)
    array([[1, 4],
           [2, 5],
           [3, 6]])

    """
    arrays = [asanyarray(arr) for arr in arrays]
    if not arrays:
        raise ValueError('need at least one array to stack')

    shapes = {arr.shape for arr in arrays}
    if len(shapes) != 1:
        raise ValueError('all input arrays must have the same shape')

    result_ndim = arrays[0].ndim + 1
    axis = normalize_axis_index(axis, result_ndim)

    sl = (slice(None),) * axis + (_nx.newaxis,)
    expanded_arrays = [arr[sl] for arr in arrays]
    return _nx.concatenate(expanded_arrays, axis=axis, out=out,
                           dtype=dtype, casting=casting)


def stack(operands: Sequence[ArrayLike], axis: int = 0) -> Array:
  """Joins a sequence of arrays along a new axis.

  Args:
    operands: a sequence of arrays to stack. All arrays must have the same shape.
    axis: the axis along which to stack the arrays.

  Returns:
    An array containing the stacked operands.

  Examples:
    >>> import jax.numpy as jnp
    >>> from jax import lax
    >>> x = jnp.array([1, 2])
    >>> y = jnp.array([3, 4])
    >>> lax.stack([x, y], axis=0)
    Array([[1, 2],
           [3, 4]], dtype=int32)
    >>> lax.stack([x, y], axis=1)
    Array([[1, 3],
           [2, 4]], dtype=int32)
  """
  arrays = [asarray(op) for op in operands]
  axis = canonicalize_axis(axis, arrays[0].ndim + 1)
  arrays = core.auto_insert_reshard(*arrays)
  return stack_p.bind(*arrays, axis=axis)


def stack(arrays: np.ndarray | Array | Sequence[ArrayLike],
          axis: int = 0, out: None = None, dtype: DTypeLike | None = None) -> Array:
  """Join arrays along a new axis.

  JAX implementation of :func:`numpy.stack`.

  Args:
    arrays: a sequence of arrays to stack; each must have the same shape. If a
      single array is given it will be treated equivalently to
      `arrays = unstack(arrays)`, but the implementation will avoid explicit
      unstacking.
    axis: specify the axis along which to stack.
    out: unused by JAX
    dtype: optional dtype of the resulting array. If not specified, the dtype
      will be determined via type promotion rules described in :ref:`type-promotion`.

  Returns:
    the stacked result.

  See also:
    - :func:`jax.numpy.unstack`: inverse of ``stack``.
    - :func:`jax.numpy.concatenate`: concatenation along existing axes.
    - :func:`jax.numpy.vstack`: stack vertically, i.e. along axis 0.
    - :func:`jax.numpy.hstack`: stack horizontally, i.e. along axis 1.
    - :func:`jax.numpy.dstack`: stack depth-wise, i.e. along axis 2.
    - :func:`jax.numpy.column_stack`: stack columns.

  Examples:
    >>> x = jnp.array([1, 2, 3])
    >>> y = jnp.array([4, 5, 6])
    >>> jnp.stack([x, y])
    Array([[1, 2, 3],
           [4, 5, 6]], dtype=int32)
    >>> jnp.stack([x, y], axis=1)
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)

    :func:`~jax.numpy.unstack` performs the inverse operation:

    >>> arr = jnp.stack([x, y], axis=1)
    >>> x, y = jnp.unstack(arr, axis=1)
    >>> x
    Array([1, 2, 3], dtype=int32)
    >>> y
    Array([4, 5, 6], dtype=int32)
  """
  if not len(arrays):
    raise ValueError("Need at least one array to stack.")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.stack is not supported.")
  if isinstance(arrays, (np.ndarray, Array)):
    axis = _canonicalize_axis(axis, arrays.ndim)
    return concatenate(expand_dims(arrays, axis + 1), axis=axis, dtype=dtype)
  else:
    arrays = util.ensure_arraylike_tuple("stack", arrays)
    if dtype is not None:
      arrays = [asarray(a, dtype=dtype) for a in arrays]
    else:
      arrays = util.promote_dtypes(*arrays)
    return lax.stack(arrays, axis=axis)


def stack(tensors: Any, new_dim: Any, dim: int = 0) -> _Tensor:
    """
    Stack tensors along a new dimension.

    Args:
        tensors: Sequence of tensors to stack
        new_dim: The new Dim to create for stacking
        dim: The dimension position to insert the new dimension (default: 0)

    Returns:
        Stacked tensor with the new dimension
    """
    if not tensors:
        raise ValueError("stack expects a non-empty sequence of tensors")

    # Check if new_dim is a Dim object
    if not isinstance(new_dim, Dim):
        # Fall back to regular torch.stack
        result = torch.stack(tensors, dim=dim)
        return result  # type: ignore[return-value]

    # Collect all result_levels from input tensors
    result_levels = []
    infos = []

    for t in tensors:
        info = TensorInfo.create(t, ensure_batched=False, ensure_present=False)
        infos.append(info)
        for level in info.levels:
            if level not in result_levels:
                result_levels.append(level)

    # Set the new_dim size to match number of tensors
    new_dim.size = len(tensors)

    # Match all tensors to the common level structure using _match_levels
    inputs = []
    for info in infos:
        if info.tensor is None:
            raise AssertionError("Cannot stack tensors with None tensor data")
        matched_tensor = _match_levels(info.tensor, info.levels, result_levels)
        inputs.append(matched_tensor)

    # Calculate ndim and resolve the dim parameter
    ndim = ndim_of_levels(result_levels)
    rawdim = 0
    if dim is not None and not (isinstance(dim, int) and dim == 0):
        from ._wrap import _wrap_dim

        d = _wrap_dim(dim, ndim, False)
        try:
            idx = result_levels.index(d)
        except ValueError:
            raise TypeError(f"Dimension {dim} does not exist in inputs") from None
        rawdim = idx

    # Stack tensors at the resolved dimension
    result = torch.stack(inputs, rawdim)

    # Insert new dimension entry at the correct position
    result_levels.insert(rawdim, DimEntry(new_dim))

    # Return as a first-class tensor
    tensor_result = Tensor.from_positional(
        result, result_levels, infos[0].has_device if infos else True
    )
    return tensor_result  # type: ignore[return-value]

