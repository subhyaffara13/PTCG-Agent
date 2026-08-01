
def _summarize_array_data_unconditionally(array: jax.Array) -> list[str]:
  """Summarized the data of a JAX array."""
  assert jax is not None, "JAX is not available."
  jnp = jax.numpy
  output_parts = []
  # This is required if treescope is invoked inside jitted function.
  with jax.core.ensure_compile_time_eval():
    is_floating = _is_subdtype(array.dtype, jnp.floating)
    is_integer = _is_subdtype(array.dtype, jnp.integer)
    is_bool = _is_subdtype(array.dtype, jnp.bool_)
    if not (is_floating or is_integer or is_bool):
      # Non-numeric non-bool data type (perhaps JAX PRNG key dtype). Can't
      # summarize values.
      return []

    if array.size < SUMMARIZE_USING_NUMPY_THRESHOLD:
      stat = _compute_summary(array, is_floating, is_integer, is_bool, xnp=np)
    else:
      compute_summary = jax.jit(_compute_summary, static_argnums=(1, 2, 3))
      stat = compute_summary(array, is_floating, is_integer, is_bool)
      # Get values in parallel.
      stat = jax.device_get(stat)

    # pylint: disable=inconsistent-quotes
    if is_floating and stat["any_finite"]:
      output_parts.append(f" ≈{stat['mean']:.2} ±{stat['std']:.2}")
      output_parts.append(f" [≥{stat['nanmin']:.2}, ≤{stat['nanmax']:.2}]")

    if is_integer:
      output_parts.append(f" [≥{stat['min']:_d}, ≤{stat['max']:_d}]")
    # pylint: enable=inconsistent-quotes

    def append_if_present(output_parts, *names):
      for name in names:
        if stat[name]:
          output_parts.append(f" {name}:{stat[name]:_d}")

    if is_floating or is_integer:
      append_if_present(output_parts, "zero", "nonzero")
    if is_floating:
      append_if_present(output_parts, "nan", "inf", "-inf")

    if is_bool:
      append_if_present(output_parts, "true", "false")
    return output_parts

