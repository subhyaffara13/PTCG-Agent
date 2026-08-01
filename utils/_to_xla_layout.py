
def _to_xla_layout(layout: Layout | None | AutoLayoutSingleton,
                   aval: core.AbstractValue) -> str | None:
  if layout is None:
    return None
  if isinstance(layout, AutoLayoutSingleton):
    return "auto"
  if aval is core.abstract_token:
    return None
  return str(layout._to_xla_layout(aval.dtype))  # pyrefly: ignore[missing-attribute]

