
def require_unanimous_scalar_result(
    result: jax.Array, *, op_name: str
) -> Any:
  """Returns a unanimous scalar value from workers or raises."""
  values = scalar_result_values(result, op_name=op_name)
  unique_values = set(values)
  if len(unique_values) != 1:
    raise RuntimeError(
        f'{op_name}: workers disagreed on scalar result: '
        f'{sorted(unique_values)} (sample={values[:8]})'
    )
  return values[0]

