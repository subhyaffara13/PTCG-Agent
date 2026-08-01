
def _make_select_and_scatter_add_harness(name,
                                         *,
                                         shape=(2, 4, 6),
                                         dtype=np.float32,
                                         select_prim=lax.ge_p,
                                         window_dimensions=(2, 2, 2),
                                         window_strides=(1, 1, 1),
                                         padding=((0, 0), (0, 0), (0, 0)),
                                         nb_inactive_dims=0):
  ones = (1,) * len(shape)
  cotangent_shape = api.eval_shape(
      lambda x: lax_windowed_reductions._select_and_gather_add(
          x, x, lax.ge_p, window_dimensions, window_strides, padding,
          ones, ones),
      np.ones(shape, dtype)).shape
  define(
      lax.select_and_scatter_add_p,
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_selectprim={select_prim}_windowdimensions={window_dimensions}_windowstrides={window_strides}_{padding=!s}",
      lax_windowed_reductions._select_and_scatter_add, [
          RandArg(cotangent_shape, dtype),
          RandArg(shape, dtype),
          StaticArg(select_prim),
          StaticArg(window_dimensions),
          StaticArg(window_strides),
          StaticArg(padding)
      ],
      jax_unimplemented=[
          Limitation(
              "works only for 2 or more inactive dimensions",
              devices="tpu",
              enabled=(nb_inactive_dims < 2))
      ],
      shape=shape,
      dtype=dtype,
      select_prim=select_prim,
      window_dimensions=window_dimensions,
      window_strides=window_strides,
      padding=padding)

