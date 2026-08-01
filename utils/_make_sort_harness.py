
def _make_sort_harness(name,
                       *,
                       operands=None,
                       shape=(5, 7),
                       dtype=np.float32,
                       dimension=0,
                       is_stable=False,
                       num_keys=1):
  if operands is None:
    operands = [RandArg(shape, dtype)]
  define(
      lax.sort_p,
      f"{name}_num_arrays={len(operands)}_shape={jtu.format_shape_dtype_string(operands[0].shape, operands[0].dtype)}_axis={dimension}_isstable={is_stable}_{num_keys=}",
      lambda *args: lax.sort_p.bind(
          *args[:-3], dimension=args[-3], is_stable=args[-2], num_keys=args[-1]
      ), [
          *operands,
          StaticArg(dimension),
          StaticArg(is_stable),
          StaticArg(num_keys)
      ],
      shape=operands[0].shape,
      dimension=dimension,
      dtype=operands[0].dtype,
      is_stable=is_stable,
      num_keys=num_keys,
      num_arrays=len(operands))

