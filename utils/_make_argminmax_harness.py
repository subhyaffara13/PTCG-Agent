
def _make_argminmax_harness(prim,
                            name,
                            *,
                            shape=(15,),
                            dtype=np.float32,
                            axes=(0,),
                            index_dtype=np.int32,
                            arr=None,
                            works_without_xla=True):
  arr = arr if arr is not None else RandArg(shape, dtype)
  dtype, shape = arr.dtype, arr.shape
  index_dtype = dtypes.canonicalize_dtype(index_dtype)
  for enable_xla in [True, False]:
    define(
        prim,
        f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_{axes=}_indexdtype={index_dtype}_enable_xla={enable_xla}",
        lambda arg: prim.bind(arg, axes=axes, index_dtype=index_dtype), [arr],
        shape=shape,
        dtype=dtype,
        axes=axes,
        index_dtype=index_dtype,
        prim=prim,
        enable_xla=enable_xla)

