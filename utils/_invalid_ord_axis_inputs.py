
def _invalid_ord_axis_inputs(ord_axis_keepdims):
  ord_, axis = ord_axis_keepdims[0], ord_axis_keepdims[1]
  return any((
      (ord_ == 0 and axis is None),
      (isinstance(ord_, float) and axis is None),
      (isinstance(ord_, str) and axis is not None),
  ))

