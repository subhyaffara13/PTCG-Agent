
def _make_comparator_harness(name,
                             *,
                             dtype=np.float32,
                             op=lax.eq_p,
                             op_name="eq",
                             lhs_shape=(),
                             rhs_shape=()):
  define(
      op_name,
      f"{name}_lhs={jtu.format_shape_dtype_string(lhs_shape, dtype)}_rhs={jtu.format_shape_dtype_string(rhs_shape, dtype)}",
      lambda *args: op(*args),
      [RandArg(lhs_shape, dtype),
       RandArg(rhs_shape, dtype)],
      op=op,
      op_name=op_name,
      lhs_shape=lhs_shape,
      rhs_shape=rhs_shape,
      dtype=dtype)

