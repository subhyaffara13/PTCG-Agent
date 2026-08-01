
def is_scalar_pred(pred) -> bool:
  return (isinstance(pred, bool) or
          isinstance(pred, Array) and pred.shape == () and
          pred.dtype == np.dtype('bool'))

