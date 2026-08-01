
def _make_dot_general_harness(name,
                              *,
                              lhs_shape=(3, 4),
                              rhs_shape=(4, 2),
                              lhs_dtype=np.float32,
                              rhs_dtype=np.float32,
                              precision=None,
                              dimension_numbers=(((1,), (0,)), ((), ())),
                              preferred_element_type=None,
                              enable_xla=True):
  suffix = ""
  if precision is not None:
    suffix += f"_{precision=}"
  if preferred_element_type is not None:
    suffix += f"_preferred={jtu.dtype_str(preferred_element_type)}"

  if (
      preferred_element_type in (np.float64, np.int64, np.complex128)
      and not config.enable_x64.value
  ):
    return

  define(
      lax.dot_general_p,
      f"{name}_lhs={jtu.format_shape_dtype_string(lhs_shape, lhs_dtype)}_rhs={jtu.format_shape_dtype_string(rhs_shape, rhs_dtype)}_dimensionnumbers={dimension_numbers}{suffix}_enable_xla={enable_xla}"
      .replace(" ", ""),
      lax.dot_general,
      [
          RandArg(lhs_shape, lhs_dtype),
          RandArg(rhs_shape, rhs_dtype),
          StaticArg(dimension_numbers),
          StaticArg(precision),
          StaticArg(preferred_element_type)
      ],
      dtype=lhs_dtype,
      rhs_dtype=rhs_dtype,
      lhs_shape=lhs_shape,
      rhs_shape=rhs_shape,
      dimension_numbers=dimension_numbers,
      precision=precision,
      preferred_element_type=preferred_element_type,
      enable_xla=enable_xla,
      jax_unimplemented=[
          Limitation("preferred_element_type must match dtype for floating point",
                     devices="gpu",
                     dtypes=[np.float16, dtypes.bfloat16, np.float32, np.float64, np.complex64, np.complex128],
                     enabled=(preferred_element_type is not None and preferred_element_type != lhs_dtype)),
          Limitation("preferred_element_type must be floating for integer dtype",
                     devices="gpu",
                     dtypes=[np.int8, np.uint8, np.int16, np.uint16,
                             np.int32, np.uint32, np.int64, np.uint64],
                     enabled=(preferred_element_type is not None
                              and preferred_element_type in [
                                np.float16, dtypes.bfloat16, np.float32,
                                np.float64, np.complex64, np.complex128]),
                     skip_run=True),  # skip run because we get internal XLA error
     ])

