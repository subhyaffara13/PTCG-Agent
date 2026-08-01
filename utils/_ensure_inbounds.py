
def _ensure_inbounds(allow_invalid: bool, num_args: int, argnums: Sequence[int]
                     ) -> tuple[int, ...]:
  """Ensure argnum is within bounds. Also resolves negative argnums."""
  result = []
  for i in argnums:
    if i >= num_args and allow_invalid: continue
    if not -num_args <= i < num_args:
      raise ValueError(
          "Positional argument indices, e.g. for `static_argnums`, must have "
          "value greater than or equal to -len(args) and less than len(args), "
          f"but got value {i} for len(args) == {num_args}.")
    result.append(i % num_args)  # Resolve negative
  return tuple(result)


def _ensure_inbounds(allow_invalid: bool, num_args: int, argnums: Sequence[int]
                     ) -> tuple[int, ...]:
  """Ensure argnum is within bounds. Also resolves negative argnums."""
  result = []
  for i in argnums:
    if i >= num_args and allow_invalid: continue
    if not -num_args <= i < num_args:
      raise ValueError(
          "Positional argument indices, e.g. for `static_argnums`, must have "
          "value greater than or equal to -len(args) and less than len(args), "
          f"but got value {i} for len(args) == {num_args}.")
    result.append(i % num_args)  # Resolve negative
  return tuple(result)

