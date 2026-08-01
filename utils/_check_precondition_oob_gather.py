
def _check_precondition_oob_gather(
    shape: tuple[int, ...], gather_indices: ArrayLike
) -> None:
  """Check for out of bounds errors before calling `lax.gather`."""
  if config.error_checking_behavior_oob.value == "ignore":
    return
  if not np.size(gather_indices):
    return

  gather_indices = array_constructors.array(gather_indices)
  shape_arr = array_constructors.array(shape, dtype=gather_indices.dtype)
  error_check_lib.set_error_if(
      ufuncs.logical_or(
          reductions.min(gather_indices) < -shape_arr,
          reductions.max(gather_indices) >= shape_arr,
      ),
      "Out of bounds encountered before calling `lax.gather`",
  )

