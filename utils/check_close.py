
def check_close(xs, ys, atol=None, rtol=None, err_msg=''):
  assert_close = partial(_assert_numpy_close, atol=atol, rtol=rtol,
                         err_msg=err_msg)
  tree_map(assert_close, xs, ys)

