
def _reducer_from_pyfunc(py_binop, init_val):
  def reducer(operand, axis=0):
    axis = range(np.ndim(operand)) if axis is None else axis
    result = np.full(np.delete(np.shape(operand), axis), init_val,
                      dtype=np.asarray(operand).dtype)
    for idx, _ in np.ndenumerate(operand):
      out_idx = tuple(np.delete(idx, axis))
      result[out_idx] = py_binop(result[out_idx], operand[idx])
    return result
  return reducer

