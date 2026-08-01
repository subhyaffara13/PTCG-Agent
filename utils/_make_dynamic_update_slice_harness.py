
def _make_dynamic_update_slice_harness(name,
                                       shape=(3,),
                                       start_indices=(1,),
                                       dtype=np.float32,
                                       update_shape=(1,)):
  for enable_xla in [False, True]:
    define(
        lax.dynamic_update_slice_p,
        (
            f"{name}_operand={jtu.format_shape_dtype_string(shape, dtype)}"
            f"_update={jtu.format_shape_dtype_string(update_shape, dtype)}"
            f"_{start_indices=}_{enable_xla=}"),
        lax.dynamic_update_slice,
        [
            RandArg(shape, dtype),
            RandArg(update_shape, dtype),
            np.array(start_indices)
        ],
        dtype=dtype,
        shape=shape,
        start_indices=start_indices,
        update_shape=update_shape,
        enable_xla=enable_xla)

