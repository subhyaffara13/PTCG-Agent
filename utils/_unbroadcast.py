
def _unbroadcast(aval, x):
  if not isinstance(aval, ShapedArray):
    raise TypeError(
        'transpose with implicit broadcasting of unshaped values. Got'
        f' {type(aval)}')
  x_shape = np.shape(x)
  if (core.definitely_equal_shape(aval.shape, x_shape) and
      aval.sharding == typeof(x).sharding):
    return x
  assert not aval.shape or len(x_shape) == len(aval.shape)
  if not aval.shape:
    return reduce_sum(x, list(range(len(x_shape))))
  else:
    dims = [i for i, (a, b) in enumerate(zip(x_shape, aval.shape))
            if not core.definitely_equal(a, b)]
    if config.enable_checks.value:
      assert all(aval.shape[i] == 1 for i in dims)
    x = reduce_sum(x, dims) if dims else x
    return reshape(x, aval.shape, out_sharding=aval.sharding)

