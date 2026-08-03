from typing import Any, Callable

def global_aval_to_result_handler(
    aval: core.AbstractValue, out_sharding, committed: bool
) -> Callable[[Sequence[xc.ArrayImpl]], Any]:
  """Returns a function for handling the raw buffers of a single output aval.

  Args:
    aval: The global output AbstractValue.
    out_axis_resources: A PartitionSpec specifying the sharding of outputs.
      Used for creating GSDAs.
    global_mesh: The global device mesh that generated this output. Used
      for creating GSDAs.

  Returns:
    A function for handling the Buffers that will eventually be produced
    for this output. The function will return an object suitable for returning
    to the user, e.g. an Array.
  """
  try:
    return global_result_handlers[type(aval)](aval, out_sharding, committed)
  except KeyError as err:
    raise TypeError(
        f"No pxla_result_handler for type: {type(aval)}") from err

