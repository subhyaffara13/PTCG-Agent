
def cumred_reduce_window_impl(window_reduce: Callable, x, *, axis: int,
                              reverse: bool):
  n = x.shape[axis]
  if n == 0:
    return x
  padding = [(0, 0)] * x.ndim
  padding[axis] = (0, n - 1) if reverse else (n - 1, 0)
  strides = [1] * x.ndim
  window_dims = [1] * x.ndim
  window_dims[axis] = n
  return window_reduce(x, window_dims, strides, padding)

