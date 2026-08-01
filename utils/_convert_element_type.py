
def _convert_element_type(x: TensorBox, dtype: torch.dtype):
    if dtype.is_complex or x.get_dtype().is_complex:
        if x.get_size():
            # Decompose since aa aten fallback is more friendly for c++ codegen.
            # This decomposition doesn't work for empty tensor, which needs more investigation.
            dst = empty_like(x, dtype=dtype)
            ir.InplaceCopyFallback.create(dst, x)
            return dst
        else:
            return fallback_handler(
                prims.convert_element_type.default, add_to_fallback_set=False
            )(x, dtype)
    src_dtype = x.get_dtype()
    low_pr_fp = (torch.bfloat16, torch.float16)
    use_compute_types = not (
        config.emulate_precision_casts
        and (src_dtype in low_pr_fp or dtype in low_pr_fp)
    )
    return to_dtype(x, dtype, copy=True, use_compute_types=use_compute_types)


def _convert_element_type(
    operand: ArrayLike | literals.TypedNdArray,
    new_dtype: DType | None = None,
    weak_type: bool = False,
    sharding: Sharding | None = None,
    warn_on_complex_to_real_cast: bool = True):
  jax_array_method = getattr(operand, "__jax_array__", None)
  if jax_array_method is not None:
    operand = jax_array_method()

  old_dtype = dtypes.dtype(operand)
  weak_type = bool(weak_type)

  if (isinstance(new_dtype, dtypes.ExtendedDType) or
      isinstance(old_dtype, dtypes.ExtendedDType)):
    if new_dtype == old_dtype:
      if sharding is None:
        return operand
      if (isinstance(operand, core.Tracer) and
          operand.aval.sharding == sharding):  # pyrefly: ignore[missing-attribute]
        return operand
    if sharding is not None or weak_type:
      raise NotImplementedError
    if (isinstance(new_dtype, dtypes.ExtendedDType) and
        isinstance(old_dtype, dtypes.ExtendedDType)):
      old_rep_dtype = core.physical_element_aval(old_dtype).dtype
      new_rep_dtype = core.physical_element_aval(new_dtype).dtype
      raise ValueError(
          "cannot directly convert between extended dtypes: from "
          f"{dtype_to_string(old_dtype)} to {dtype_to_string(new_dtype)}. "
          "Instead, convert to and from their representation dtypes, e.g.:\n"
          f"{dtype_to_string(old_dtype)} -> {dtype_to_string(old_rep_dtype)} "
          f"-> {dtype_to_string(new_rep_dtype)} -> {dtype_to_string(new_dtype)}")

    if isinstance(new_dtype, dtypes.ExtendedDType):
      return to_edtype_p.bind(operand, edtype=new_dtype)
    return from_edtype_p.bind(operand, dtype=np.dtype(new_dtype))

  old_weak_type = dtypes.is_weakly_typed(operand)
  if new_dtype is None:
    new_dtype = old_dtype
  else:
    assert isinstance(new_dtype, DType), new_dtype

  if sharding is not None and not isinstance(sharding, Sharding):
    raise ValueError(f'{sharding=} must be an instance of jax.sharding.Sharding')

  if (warn_on_complex_to_real_cast and
      dtypes.issubdtype(old_dtype, np.complexfloating) and
      not dtypes.issubdtype(new_dtype, np.complexfloating)):
    msg = "Casting complex values to real discards the imaginary part"
    warnings.warn(msg, np.exceptions.ComplexWarning, stacklevel=2)

  # Python has big integers, but convert_element_type(2 ** 100, np.float32) need
  # not be an error since the target dtype fits the value. Handle this case by
  # converting to a NumPy array before calling bind. Without this step, we'd
  # first canonicalize the input to a value of dtype int32 or int64, leading to
  # an overflow error.
  if type(operand) is int and new_dtype != dtypes.float0:
    arr = np.asarray(operand).astype(new_dtype)
    aval = core.ShapedArray(arr.shape, arr.dtype, weak_type=weak_type)
    operand = literals.TypedNdArray(arr, aval=aval)

  if isinstance(operand, (bool, int, float, builtins.complex, np.generic)):
    if sharding is None:
      if old_dtype == new_dtype and old_weak_type == weak_type:
        return stage(operand)  # pyrefly: ignore[bad-argument-type]
      elif not weak_type and new_dtype != dtypes.float0 and not (
          # TODO(phawkins): remove this block so we raise on inf/nan to int
          # conversion. This code exists to avoid breaking users.
          isinstance(operand, (float, builtins.complex, np.inexact))
          and not np.isfinite(operand)
          and dtypes.issubdtype(new_dtype, np.integer)
      ):
        aval = core.ShapedArray((), new_dtype, weak_type=weak_type)
        # TODO(phawkins): remove the try-except block here, which would be
        # a breaking change to users in the presence of overflows.
        try:
          x = literals.TypedNdArray(np.asarray(operand, dtype=new_dtype),
                                    aval=aval)
          return stage(x)
        except OverflowError:
          pass
  elif isinstance(operand, Array):
    if (old_dtype == new_dtype and old_weak_type == weak_type and
        not (isinstance(operand, core.Tracer) and core.is_concrete(operand)) and
        (sharding is None or
          (sharding._is_concrete and getattr(operand, 'sharding', None) == sharding))):
      return operand

  return convert_element_type_p.bind(
      operand, new_dtype=new_dtype, weak_type=weak_type,
      sharding=sharding)

