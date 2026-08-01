
def summarize_array_data(array: jax.Array) -> str:
  """Summarized the data of a JAX array.

  Args:
    array: The array to summarize.

  Returns:
    A string summarizing the data of the array.
  """

  output_parts = []

  if isinstance(array, jax.core.Tracer):
    output_parts.append(" - tracer.")
  elif array.is_deleted():
    output_parts.append(" - deleted!")
  elif not _is_locally_available(array):
    output_parts.append(" - multi-host array!")
  elif safe_to_summarize(array):
    output_parts.extend(_summarize_array_data_unconditionally(array))
  else:
    output_parts.append("- too large to summarize.")

  return "".join(output_parts)

