
def _check_scalar(actual, desired, *, xp=None, **kwargs):
    __tracebackhide__ = True  # Hide traceback for py.test

    if xp is None:
        xp = array_namespace(actual)

    # necessary to handle non-numpy scalars, e.g. bare `0.0` has no shape
    desired = xp.asarray(desired)

    # Only NumPy distinguishes between scalars and arrays;
    # shape check in xp_assert_* is sufficient except for shape == ()
    if not (is_numpy(xp) and desired.shape == ()):
        return

    _msg = ("Result is a NumPy 0d-array. Many SciPy functions intend to follow "
            "the convention of many NumPy functions, returning a scalar when a "
            "0d-array would be correct. The specialized `xp_assert_*` functions "
            "in the `scipy._lib._array_api_no_0d` module err on the side of "
            "caution and do not accept 0d-arrays by default. If the correct "
            "result may legitimately be a 0d-array, pass `check_0d=True`, "
            "or use the `xp_assert_*` functions from `scipy._lib._array_api`.")
    assert xp.isscalar(actual), _msg


def _check_scalar(x):
  msg = "Gradient only defined for scalar-output functions. Output {}.".format
  try:
    aval = core.typeof(x)
  except TypeError as e:
    raise TypeError(msg(f"was {x}")) from e
  else:
    if isinstance(aval, ShapedArray):
      if aval.shape != ():
        raise TypeError(msg(f"had shape: {aval.shape}"))
    else:
      raise TypeError(msg(f"had abstract value {aval}"))

