
def _make_reduce_window_harness(name,
                                *,
                                shape=(4, 6),
                                base_dilation=(1, 1),
                                computation=lax.add,
                                window_dimensions=(2, 2),
                                window_dilation=(1, 1),
                                init_value=0,
                                window_strides=(1, 1),
                                dtype=np.float32,
                                padding=((0, 0), (0, 0)),
                                requires_xla=False):
  prim_name = f"reduce_window_{computation.__name__}"
  limitations = []
  xla_opts = [True] if requires_xla else [True, False]

  for enable_xla in xla_opts:
    define(
        prim_name,
        f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_initvalue={init_value}_windowdimensions={window_dimensions}_windowstrides={window_strides}_{padding=!s}_basedilation={base_dilation}_windowdilation={window_dilation}_enablexla={enable_xla}"
        .replace(" ", ""),
        lax.reduce_window,
        [
            RandArg(shape, dtype),
            # Must be static to trigger the picking of the reducers
            StaticArg(np.array(init_value, dtype=dtype)),
            StaticArg(computation),
            StaticArg(window_dimensions),
            StaticArg(window_strides),
            StaticArg(padding),
            StaticArg(base_dilation),
            StaticArg(window_dilation)
        ],
        jax_unimplemented=limitations,
        shape=shape,
        dtype=dtype,
        init_value=np.array(init_value, dtype=dtype),
        computation=computation,
        window_dimensions=window_dimensions,
        window_strides=window_strides,
        padding=padding,
        base_dilation=base_dilation,
        window_dilation=window_dilation,
        enable_xla=enable_xla)

