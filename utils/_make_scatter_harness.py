
def _make_scatter_harness(name,
                          *,
                          shape=(5,),
                          f_lax=lax.scatter_min,
                          indices_are_sorted=False,
                          unique_indices=False,
                          scatter_indices=np.array([[0], [2]]),
                          update_shape=(2,),
                          mode=lax.GatherScatterMode.FILL_OR_DROP,
                          dtype=np.float32,
                          dimension_numbers=lax.ScatterDimensionNumbers(
                              update_window_dims=(), inserted_window_dims=(0,),
                              scatter_dims_to_operand_dims=(0,)),
                          enable_and_disable_xla=False):
  xla_options = [True, False] if enable_and_disable_xla else [True]

  for enable_xla in xla_options:
    define(
        f_lax.__name__,
        f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_scatterindices={scatter_indices.tolist()}_updateshape={update_shape}_{dimension_numbers=}_indicesaresorted={indices_are_sorted}_uniqueindices={unique_indices}_{mode=!s}_enablexla={enable_xla}"
        .replace(" ", ""),
        partial(
            f_lax,
            indices_are_sorted=indices_are_sorted,
            unique_indices=unique_indices,
            mode=mode), [
                RandArg(shape, dtype),
                StaticArg(scatter_indices),
                RandArg(update_shape, dtype),
                StaticArg(dimension_numbers)
            ],
        jax_unimplemented=[
            Limitation(
                "unimplemented",
                dtypes=[np.bool_],
                enabled=(f_lax in [lax.scatter_add, lax.scatter_mul])),
        ],
        f_lax=f_lax,
        shape=shape,
        dtype=dtype,
        scatter_indices=scatter_indices,
        update_shape=update_shape,
        dimension_numbers=dimension_numbers,
        indices_are_sorted=indices_are_sorted,
        unique_indices=unique_indices,
        mode=mode,
        enable_xla=enable_xla)

