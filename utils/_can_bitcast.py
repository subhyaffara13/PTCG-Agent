
def _can_bitcast(dtype, target_dtype):

  def _to_equivalence_class(dtype):
    if dtypes.issubdtype(dtype, np.integer):
      return dtypes.iinfo(dtype).bits
    elif dtypes.issubdtype(dtype, np.floating):
      return dtypes.finfo(dtype).bits
    else:
      assert dtype == np.bool_ or dtypes.issubdtype(dtype, np.complexfloating)
      # Complex and boolean types can only be cast to themselves
      return np.dtype(dtype).name

  return _to_equivalence_class(dtype) == _to_equivalence_class(target_dtype)

