
def _make_reduce_harness(name, *,
                         shape=(4, 6),  # The shape of all operands
                         nr_operands=1,  # How many operands
                         computation=lax.add,  # Takes Tuple(op1, [op2,]) and Tuple(init_val1, [init_val2]). Returns Tuple(out_val1, [out_val2]).
                         dimensions: Sequence[int] = (0,),
                         init_value=0,  # The init value for first operand
                         dtype=np.float32):  # The dtype of first operand
  def reducer(*args):
    init_val = np.array(init_value, dtype=dtype)
    init_values: list[np.ndarray] = [init_val]
    if nr_operands == 2:
      init_values.append(np.array(0, dtype=np.int32))
    return lax.reduce(args[0:nr_operands], tuple(init_values),
                      computation, dimensions)
  define(
      lax.reduce_p,
      f"gen_{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_initvalue={init_value}_{nr_operands=}_{dimensions=}".replace(" ", ""),
      reducer,
      [
          RandArg(shape, dtype),
          # Second operand (optional, always i32). We cannot mix multiple float
          # types in XLA.
          RandArg(shape, np.int32),
      ],
      shape=shape,
      dtype=dtype,
      init_value=init_value,
      computation=computation,
      dimensions=dimensions)

