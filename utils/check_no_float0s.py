
def check_no_float0s(fun_name: str, *args: Any):
  """Check if none of the args have dtype float0."""
  if any(dtypes.dtype(arg) == dtypes.float0 for arg in args):
    raise TypeError(
        f"Called {fun_name} with a float0 array. "
        "float0s do not support any operations by design because they "
        "are not compatible with non-trivial vector spaces. No implicit dtype "
        "conversion is done. You can use np.zeros_like(arr, dtype=np.float) "
        "to cast a float0 array to a regular zeros array. \n"
        "If you didn't expect to get a float0 you might have accidentally "
        "taken a gradient with respect to an integer argument.")

