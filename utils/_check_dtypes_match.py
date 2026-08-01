
def _check_dtypes_match(xs, ys):
  def _assert_dtypes_match(x, y):
    if config.enable_x64.value:
      assert _dtype(x) == _dtype(y)
    else:
      assert (_dtypes.canonicalize_dtype(_dtype(x)) ==
              _dtypes.canonicalize_dtype(_dtype(y)))
  tree_map(_assert_dtypes_match, xs, ys)

