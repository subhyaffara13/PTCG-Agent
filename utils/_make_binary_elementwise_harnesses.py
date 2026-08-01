
def _make_binary_elementwise_harnesses(prim,
                                       dtypes,
                                       default_dtype=np.float32,
                                       broadcasting_dtypes=None,
                                       jax_unimplemented=lambda **kwargs: []):

  def _make(name, *, shapes=((20, 20), (20, 20)), dtype):
    lhs_shape, rhs_shape = shapes
    define(
        prim,
        f"{name}_lhs={jtu.format_shape_dtype_string(lhs_shape, dtype)}_rhs={jtu.format_shape_dtype_string(rhs_shape, dtype)}",
        prim.bind, [RandArg(lhs_shape, dtype),
                    RandArg(rhs_shape, dtype)],
        jax_unimplemented=jax_unimplemented(
            dtype=dtype, prim=prim, shapes=shapes),
        prim=prim,
        dtype=dtype,
        shapes=shapes)
  broadcasting_dtypes = broadcasting_dtypes or (default_dtype,)
  return (
      # Validate dtypes
      tuple(_make("dtypes", dtype=dtype) for dtype in dtypes) +
      # Validate broadcasting
      tuple(_make("broadcasting", dtype=dtype, shapes=shapes)
            for shapes in [
              ((20, 20), (1, 20)),  # broadcasting rhs
              ((1, 20), (20, 20)),  # broadcasting lhs
            ]
            for dtype in broadcasting_dtypes)
  )

