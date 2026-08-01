
def _make_select_n_harness(name,
                         *,
                         shape_pred=(2, 3),
                         shape_args=(2, 3),
                         dtype=np.float32):
  define(
      lax.select_n_p,
      f"{name}_shapepred={jtu.format_shape_dtype_string(shape_pred, np.bool_)}_shapeargs={jtu.format_shape_dtype_string(shape_args, dtype)}",
      lax.select_n, [
          RandArg(shape_pred, np.bool_),
          RandArg(shape_args, dtype),
          RandArg(shape_args, dtype)
      ],
      shape_pred=shape_pred,
      shape_args=shape_args,
      dtype=dtype)
  define(
      lax.select_n_p,
      f"{name}_shapepred={jtu.format_shape_dtype_string(shape_pred, np.int32)}_shapeargs={jtu.format_shape_dtype_string(shape_args, dtype)}",
      lax.select_n, [
          CustomArg(lambda rng: jtu.rand_int(rng, high=3)(shape_args, np.int32)),
          RandArg(shape_args, dtype),
          RandArg(shape_args, dtype),
          RandArg(shape_args, dtype),
      ],
      shape_pred=shape_pred,
      shape_args=shape_args,
      dtype=dtype)

