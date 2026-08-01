
def _make_div_rem_harness(prim,
                          name,
                          *,
                          shapes=((2,), (2,)),
                          dtype=np.float32,
                          arrs=(None, None)):
  lhs, rhs = arrs

  def _make_non_zero(rng):
    return jtu.rand_nonzero(rng)(shapes[1], dtype)

  lhs = RandArg(shapes[0], dtype) if lhs is None else lhs
  rhs_shape = rhs.shape if rhs is not None else shapes[1]
  rhs_dtype = rhs.dtype if rhs is not None else dtype
  rhs = CustomArg(_make_non_zero) if rhs is None else rhs

  define(
      prim,
      f"{name}_lhs={jtu.format_shape_dtype_string(lhs.shape, lhs.dtype)}_rhs={jtu.format_shape_dtype_string(rhs_shape, rhs_dtype)}",
      prim.bind, [lhs, rhs],
      dtype=dtype,
      lhs=lhs,
      rhs=rhs,
      prim=prim)

