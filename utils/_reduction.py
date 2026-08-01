
def _reduction(
    a: TensorLikeType,
    prim: Callable,
    *,
    has_identity: bool = True,
    accepts_dim_tuple: bool = True,  # to handle min/argmin that accept single dim only
    dims: DimsType | None = None,
    keepdims: bool = False,
    dtype: torch.dtype | None = None,  # should be specified for ops that support it
    out: Tensor | None = None,
    output_dtype_kind: REDUCTION_OUTPUT_TYPE_KIND,
) -> TensorLikeType:  # it is usually SAME, but I want
    # ref writers to actually think about what to put here
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")
    if a.ndim > 64:
        raise RuntimeError(
            f"Received a tensor with {a.ndim} dimensions, but only tensors with up to 64 dims are supported!"
        )

    if out is not None:
        if not isinstance(out, TensorLike):
            raise AssertionError(f"out must be TensorLike, got {type(out)}")
        if dtype is not None:
            # TODO - this is true for eager mode currently, but it's wrong behavior for complex norms
            if dtype != out.dtype:
                raise RuntimeError(
                    "dtype argument and out dtype must match in reduction"
                )
    if not accepts_dim_tuple:
        if not (dims is None or isinstance(dims, Dim)):
            raise AssertionError(f"dims must be None or Dim, got {type(dims)}")
    if isinstance(dims, Dim):
        dims = (dims,)  # type: ignore[assignment]
    dims = utils.reduction_dims(a.shape, dims)
    if not has_identity:
        from torch.fx.experimental.symbolic_shapes import sym_and

        valid_shape = a.ndim == 0 or sym_and(*(a.shape[i] > 0 for i in dims))
        torch._check(
            valid_shape,
            lambda: "reducing over zero-size dimension for reduction operation without identity",
        )

    computation_dtype, result_dtype = utils.reduction_dtypes(
        a, output_dtype_kind, dtype
    )
    a = _maybe_convert_to_dtype(a, computation_dtype)  # type: ignore[method-assign]
    result = prim(a, dims)
    if keepdims:
        output_shape = [a.shape[i] if i not in dims else 1 for i in range(a.ndim)]
        broadcast_dims = [i for i in range(a.ndim) if i not in dims]
        result = prims.broadcast_in_dim(result, output_shape, broadcast_dims)

    if out is not None:
        if result_dtype is None:
            raise AssertionError("result_dtype should not be None when out is provided")
        if dtype is not None and result_dtype != out.dtype:
            raise RuntimeError(
                "Expected the dtype of reduction result and out to match"
            )
        out = _maybe_resize_out(out, result.shape)
        return _safe_copy_out(copy_from=result, copy_to=out)  # type: ignore[arg-type]

    if result.dtype != result_dtype and result_dtype is not None:
        result = prims.convert_element_type(result, result_dtype)

    return result


def _reduction(a: ArrayLike, name: str, op: ReductionOp, init_val: ArrayLike,
               *, has_identity: bool = True,
               preproc: Callable[[Array], Array] | None = None,
               bool_op: ReductionOp | None = None,
               upcast_f16_for_computation: bool = False,
               axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
               keepdims: bool = False, initial: ArrayLike | None = None,
               where_: ArrayLike | None = None,
               parallel_reduce: Callable[..., Array] | None = None,
               promote_integers: bool = False) -> Array:
  bool_op = bool_op or op
  # Note: we must accept out=None as an argument, because numpy reductions delegate to
  # object methods. For example `np.sum(x)` will call `x.sum()` if the `sum()` method
  # exists, passing along all its arguments.
  if out is not None:
    raise NotImplementedError(f"The 'out' argument to jnp.{name} is not supported.")
  a = ensure_arraylike(name, a)
  where_ = check_where(name, where_)
  axis = core.concrete_or_error(None, axis, f"axis argument to jnp.{name}().")

  if initial is None and not has_identity and where_ is not None:
    raise ValueError(f"reduction operation {name} does not have an identity, so to use a "
                     f"where mask one has to specify 'initial'")

  a = preproc(a) if preproc else a
  pos_dims, dims = _reduction_dims(a, axis)

  if initial is None and not has_identity:
    shape = np.shape(a)
    if not _all(shape[d] >= 1 for d in pos_dims):
      raise ValueError(f"zero-size array to reduction operation {name} which has no identity")

  result_dtype: DType
  if dtype is None:
    result_dtype = a.dtype
    if promote_integers:
      result_dtype = _promote_integer_dtype(result_dtype)
  else:
    result_dtype = dtypes.check_and_canonicalize_user_dtype(dtype, name)

  if upcast_f16_for_computation and dtypes.issubdtype(result_dtype, np.inexact):
    computation_dtype = _upcast_f16(result_dtype)
  else:
    computation_dtype = result_dtype
  a = lax.convert_element_type(a, computation_dtype)
  op = op if computation_dtype != np.bool_ else bool_op
  # NB: in XLA, init_val must be an identity for the op, so the user-specified
  # initial value must be applied afterward.
  init_val = _reduction_init_val(a, init_val)
  if where_ is not None:
    a = _where(where_, a, init_val)
  if pos_dims is not dims:
    if parallel_reduce is None:
      raise NotImplementedError(f"Named reductions not implemented for jnp.{name}()")
    result = parallel_reduce(a, dims)
  else:
    result = lax.reduce(a, init_val, op, dims)
  if initial is not None:
    initial_arr = lax.convert_element_type(initial, lax.asarray(a).dtype)
    if initial_arr.shape != ():
      raise ValueError("initial value must be a scalar. "
                       f"Got array of shape {initial_arr.shape}")
    result = op(initial_arr, result)
  if keepdims:
    result = lax.expand_dims(result, pos_dims)
  return lax.convert_element_type(result, dtype or result_dtype)

