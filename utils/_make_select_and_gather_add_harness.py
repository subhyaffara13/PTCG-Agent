
def _make_select_and_gather_add_harness(name,
                                        *,
                                        shape=(4, 6),
                                        dtype=np.float32,
                                        select_prim=lax.le_p,
                                        padding="VALID",
                                        window_dimensions=(2, 2),
                                        window_strides=(1, 1),
                                        base_dilation=(1, 1),
                                        window_dilation=(1, 1)):
  if isinstance(padding, str):
    padding = tuple(
        lax.padtype_to_pads(shape, window_dimensions, window_strides, padding))
  define(
      lax.select_and_gather_add_p,
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_selectprim={select_prim}_windowdimensions={window_dimensions}_windowstrides={window_strides}_{padding=!s}_basedilation={base_dilation}_windowdilation={window_dilation}",
      lax_windowed_reductions._select_and_gather_add, [
          RandArg(shape, dtype),
          RandArg(shape, dtype),
          StaticArg(select_prim),
          StaticArg(window_dimensions),
          StaticArg(window_strides),
          StaticArg(padding),
          StaticArg(base_dilation),
          StaticArg(window_dilation)
      ],
      shape=shape,
      dtype=dtype,
      window_dimensions=window_dimensions,
      window_strides=window_strides,
      padding=padding,
      base_dilation=base_dilation,
      window_dilation=window_dilation)

