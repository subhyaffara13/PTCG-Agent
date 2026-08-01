
def is_scalar(x):
    return isinstance(x, _SCALAR_TYPES)


def is_scalar(x):
  return isinstance(x, (int, float, np.number))

