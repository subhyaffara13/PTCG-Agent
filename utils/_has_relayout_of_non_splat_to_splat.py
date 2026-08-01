
def _has_relayout_of_non_splat_to_splat(constraints: Sequence[Constraint]) -> bool:
  """Returns whether the constraints imply a non-splat to splat relayout.

  Such relayouts are impossible and this helps shortcut the search.

  If this function returns False, this doesn't necessarily mean that there are
  no non-splat to splat relayouts, just that this is not known yet.
  """
  non_splat = non_splat_variables(constraints)
  if not non_splat:
    return False

  def is_constant_splat(e) -> bool:
    return isinstance(e, RegisterLayout) and isinstance(
        e.value, fa.WGSplatFragLayout
    )

  for constraint in constraints:
    match constraint:
      case Relayout(source=source, target=target):
        if source in non_splat and is_constant_splat(target):
          return True
      case _:
        pass
  return False

