
def _operands_to_keys(*operands, num_keys=1):
  assert len(operands) >= 2 and len(operands) % 2 == 0, operands
  assert len(operands) // 2 >= num_keys, (operands, num_keys)
  x_keys, y_keys = [], []
  for x, y in zip(operands[:2*num_keys:2], operands[1:2*num_keys:2]):
    assert x.dtype == y.dtype, (x.dtype, y.dtype)
    if dtypes.issubdtype(x.dtype, np.complexfloating):
      x_keys.extend([_canonicalize_float_for_sort(real(x)), _canonicalize_float_for_sort(imag(x))])
      y_keys.extend([_canonicalize_float_for_sort(real(y)), _canonicalize_float_for_sort(imag(y))])
    elif dtypes.issubdtype(x.dtype, np.floating):
      x_keys.append(_canonicalize_float_for_sort(x))
      y_keys.append(_canonicalize_float_for_sort(y))
    else:
      x_keys.append(x)
      y_keys.append(y)
  return x_keys, y_keys

