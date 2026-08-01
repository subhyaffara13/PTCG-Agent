
def _unique(
    fake_mode: FakeTensorMode,
    func: OpOverload,
    arg: FakeTensor,
    dim: int | None,
    sorted: bool = True,
    return_inverse: bool = False,
    return_counts: bool = False,
    *,
    unique_consecutive: bool = False,
) -> tuple[FakeTensor, FakeTensor, FakeTensor]:
    if (
        fake_mode.shape_env is None
        or not fake_mode.shape_env.allow_dynamic_output_shape_ops
    ):
        # Without symints/symfloats, cannot handle this
        raise DynamicOutputShapeException(func)

    nnz = arg.unique_consecutive_memo if unique_consecutive else arg.unique_memo

    # Do not use a memo for unique_dim
    if dim is not None or nnz is None:
        # Avoid importing sympy at a module level
        from torch.fx.experimental.symbolic_shapes import (
            _constrain_range_for_size,
            has_free_symbols,
        )

        if not has_free_symbols(arg.numel()) and arg.numel() == 0:
            # If numel is zero, then the output size must be zero.
            # In this case, we must not allocate an unbacked SymInt,
            # because if we do, it will immediately get refined to
            # zero, but this will be inconsistent with size oblivious
            # tests (which will continue to claim that the unbacked
            # symint cannot equal zero).  We could also unconditionally
            # allocate an unbacked SymInt and not refine its range,
            # but this seems more precise.
            nnz = 0
        else:
            nnz = fake_mode.shape_env.create_unbacked_symint()

            maxval = sys.maxsize - 1

            numel = arg.numel() if dim is None else arg.size(dim)
            if not has_free_symbols(numel):
                maxval = int(numel)

            _constrain_range_for_size(nnz, max=maxval)

        if dim is None:
            if unique_consecutive:
                arg.unique_consecutive_memo = nnz  # pyrefly: ignore[bad-assignment]
            else:
                arg.unique_memo = nnz  # pyrefly: ignore[bad-assignment]

    if dim is None:
        # pyrefly: ignore[no-matching-overload]
        ret = [arg.new_empty((nnz,))]
    else:
        # pyrefly: ignore[no-matching-overload]
        ret = [arg.new_empty(*arg.shape[:dim], nnz, *arg.shape[dim + 1 :])]

    return_if_dim_and_cpu = dim is not None and arg.fake_device == torch.device("cpu")
    if return_inverse or return_if_dim_and_cpu:
        inverse = arg.new_empty(
            arg.shape if dim is None else (arg.shape[dim],), dtype=torch.int64
        )
    else:
        inverse = arg.new_empty(0, dtype=torch.int64)
    ret.append(inverse)

    if return_counts or return_if_dim_and_cpu:
        counts = arg.new_empty(
            ret[0].shape if dim is None else (ret[0].shape[dim],), dtype=torch.int64
        )
    else:
        counts = arg.new_empty(0, dtype=torch.int64)
    ret.append(counts)

    return tuple(ret)


def _unique(g: jit_utils.GraphContext, input, sorted, return_inverse):
    return symbolic_helper._onnx_unsupported("_unique", input)


def _unique(
    fn: Callable[..., Generator[Any, None, None]],
) -> Callable[..., Generator[Any, None, None]]:
    @functools.wraps(fn)
    def unique(*args: Any, **kw: Any) -> Generator[Any, None, None]:
        seen: set[Any] = set()
        for item in fn(*args, **kw):
            if item not in seen:
                seen.add(item)
                yield item

    return unique


def _unique(ar: Array, axis: int, return_index: bool = False, return_inverse: bool = False,
            return_counts: bool = False, equal_nan: bool = True, size: int | None = None,
            fill_value: ArrayLike | None = None, return_true_size: bool = False
            ) -> Array | tuple[Array, ...]:
  """
  Find the unique elements of an array along a particular axis.
  """
  axis = canonicalize_axis(axis, ar.ndim)

  if ar.shape[axis] == 0 and size and fill_value is None:
    raise ValueError(
      "jnp.unique: for zero-sized input with nonzero size argument, fill_value must be specified")

  aux, mask, perm = _unique_sorted_mask(ar, axis, equal_nan)
  if size is None:
    ind = core.concrete_or_error(None, mask,
        "The error arose in jnp.unique(). " + UNIQUE_SIZE_HINT)
  else:
    ind = nonzero(mask, size=size)[0]
  result = aux[ind] if aux.size else aux
  if size is not None and fill_value is not None:
    fill_value = lax.asarray(fill_value).astype(result.dtype)
    if result.shape[0]:
      valid = lax.expand_dims(arange(size) < mask.sum(), tuple(range(1, result.ndim)))
      result = where(valid, result, fill_value)
    else:
      result = full_like(result, fill_value, shape=(size, *result.shape[1:]))
  result = moveaxis(result, 0, axis)

  ret: tuple[Array, ...] = (result,)
  if return_index:
    if aux.size:
      ret += (perm[ind],)
    else:
      ret += (perm,)
  if return_inverse:
    if aux.size:
      imask = cumsum(mask) - 1
      inv_idx = zeros(mask.shape, dtype=int)
      inv_idx = inv_idx.at[perm].set(imask)
    else:
      inv_idx = zeros(ar.shape[axis], dtype=int)
    ret += (inv_idx,)
  if return_counts:
    if aux.size:
      if size is None:
        idx = append(nonzero(mask)[0], mask.size)
      else:
        idx = nonzero(mask, size=size + 1)[0]
        idx = idx.at[1:].set(where(idx[1:], idx[1:], mask.size))
      ret += (diff(idx),)
    elif ar.shape[axis]:
      ret += (full((1,), ar.shape[axis], dtype=int),)
    else:
      ret += (empty(0, dtype=int),)
  if return_true_size:
    # Useful for internal uses of unique().
    ret += (mask.sum(),)
  return ret[0] if len(ret) == 1 else ret

