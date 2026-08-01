
def _integer_pow_dtype_rule(x, *, y):
  dtype = unop_dtype_rule(_identity, _int | _float | _complex, 'integer_pow', x)
  if y < 0 and dtypes.issubdtype(dtype, np.integer):
    raise TypeError("Integers cannot be raised to negative powers, got "
                    f"integer_pow({x}, {y})")
  return dtype

