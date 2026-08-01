
def dense_int_elements(xs) -> ir.DenseElementsAttr:
  return ir.DenseIntElementsAttr.get(np.asarray(xs, np.int64))

