
def _dims_in_range(dims, rank, op_name, name):
  for dim in dims:
    if dim < 0 or dim >= rank:
      raise TypeError(f"Invalid {name} set in {op_name} op; valid range is "
                      f"[0, {rank}); got: {dim}.")

